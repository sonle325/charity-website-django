from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
from users.models import CustomUser

class Campaign(models.Model):
    """Model for charity campaigns/events."""
    STATUS_CHOICES = (
        ('draft', _('Draft')),
        ('active', _('Active')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    )
    
    title = models.CharField(_('Title'), max_length=255)
    slug = models.SlugField(_('Slug'), max_length=255, unique=True, blank=True)
    description = models.TextField(_('Description'))
    short_description = models.TextField(_('Short Description'), max_length=500)
    target_amount = models.DecimalField(_('Target Amount'), max_digits=12, decimal_places=0)
    current_amount = models.DecimalField(_('Current Amount'), max_digits=12, decimal_places=0, default=0)
    start_date = models.DateField(_('Start Date'))
    end_date = models.DateField(_('End Date'))
    image = models.ImageField(_('Image'), upload_to='campaigns/')
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    created_by = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='campaigns_created',
        verbose_name=_('Created By')
    )
    
    class Meta:
        verbose_name = _('Campaign')
        verbose_name_plural = _('Campaigns')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('campaigns:detail', kwargs={'slug': self.slug})
    
    @property
    def progress_percentage(self):
        if self.target_amount == 0:
            return 0
        return int((self.current_amount / self.target_amount) * 100)
    
    @property
    def is_active(self):
        return self.status == 'active'


class CampaignUpdate(models.Model):
    """Model for updates on campaigns."""
    campaign = models.ForeignKey(
        Campaign, 
        on_delete=models.CASCADE, 
        related_name='updates',
        verbose_name=_('Campaign')
    )
    title = models.CharField(_('Title'), max_length=255)
    content = models.TextField(_('Content'))
    image = models.ImageField(_('Image'), upload_to='campaign_updates/', blank=True, null=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    created_by = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='campaign_updates',
        verbose_name=_('Created By')
    )
    
    class Meta:
        verbose_name = _('Campaign Update')
        verbose_name_plural = _('Campaign Updates')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.campaign.title} - {self.title}"
