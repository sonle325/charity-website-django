from django.views.generic import TemplateView, ListView
from campaigns.models import Campaign
from donations.models import Donation

class HomeView(ListView):
    """View for the homepage."""
    model = Campaign
    template_name = "core/home.html"
    context_object_name = "featured_campaigns"
    
    def get_queryset(self):
        # Get only active campaigns, ordered by creation date (newest first)
        return Campaign.objects.filter(status="active").order_by("-created_at")[:3]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add total donation amount
        total_donations = Donation.objects.filter(payment_status="completed").count()
        total_amount = Donation.objects.filter(payment_status="completed").values_list('amount', flat=True)
        context['total_donations'] = total_donations
        context['total_amount'] = sum(total_amount) if total_amount else 0
        context['total_campaigns'] = Campaign.objects.filter(status="active").count()
        return context

class AboutView(TemplateView):
    """View for the about page."""
    template_name = "core/about.html"

class ContactView(TemplateView):
    """View for the contact page."""
    template_name = "core/contact.html"
