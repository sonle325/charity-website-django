from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import CustomUser
from campaigns.models import Campaign

class Donation(models.Model):
    """Model for donations made to campaigns."""
    PAYMENT_STATUS_CHOICES = (
        ("pending", _("Pending")),
        ("completed", _("Completed")),
        ("failed", _("Failed")),
        ("refunded", _("Refunded")),
    )
    
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, # Allow anonymous donations
        related_name="donations",
        verbose_name=_("User")
    )
    campaign = models.ForeignKey(
        Campaign, 
        on_delete=models.CASCADE, 
        related_name="donations",
        verbose_name=_("Campaign")
    )
    amount = models.DecimalField(_("Amount"), max_digits=12, decimal_places=0)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    payment_status = models.CharField(
        _("Payment Status"), 
        max_length=20, 
        choices=PAYMENT_STATUS_CHOICES, 
        default="pending"
    )
    transaction_id = models.CharField(_("Transaction ID"), max_length=255, blank=True, null=True)
    is_anonymous = models.BooleanField(_("Is Anonymous"), default=False)
    # Fields for anonymous donor information if needed
    donor_name = models.CharField(_("Donor Name (Anonymous)"), max_length=255, blank=True, null=True)
    donor_email = models.EmailField(_("Donor Email (Anonymous)"), blank=True, null=True)
    
    class Meta:
        verbose_name = _("Donation")
        verbose_name_plural = _("Donations")
        ordering = ["-created_at"]
    
    def __str__(self):
        user_info = self.user.email if self.user else (self.donor_name or _("Anonymous"))
        return f"{user_info} donated {self.amount} to {self.campaign.title}"
    
    def save(self, *args, **kwargs):
        # Update campaign's current amount when a donation is completed
        is_new = self._state.adding
        old_status = None
        if not is_new:
            old_donation = Donation.objects.get(pk=self.pk)
            old_status = old_donation.payment_status
            
        super().save(*args, **kwargs)
        
        if self.payment_status == "completed" and old_status != "completed":
            self.campaign.current_amount += self.amount
            self.campaign.save(update_fields=["current_amount"])
        elif old_status == "completed" and self.payment_status != "completed":
            # Handle cases where a completed donation is changed (e.g., refunded)
            self.campaign.current_amount -= self.amount
            self.campaign.save(update_fields=["current_amount"])

