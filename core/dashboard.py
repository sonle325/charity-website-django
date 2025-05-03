from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum, Count, Avg, F, Q
from django.db.models.functions import TruncMonth, TruncDay
from django.utils import timezone
from datetime import timedelta

from donations.models import Donation
from campaigns.models import Campaign

class StaffRequiredMixin(UserPassesTestMixin):
    """Mixin to require user to be staff."""
    def test_func(self):
        return self.request.user.is_staff

class DashboardView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    """Admin dashboard view with summary statistics."""
    template_name = "core/dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Tổng quan
        context['total_campaigns'] = Campaign.objects.count()
        context['active_campaigns'] = Campaign.objects.filter(status='active').count()
        context['total_donations'] = Donation.objects.filter(payment_status='completed').count()
        context['total_amount'] = Donation.objects.filter(payment_status='completed').aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Thống kê theo thời gian (30 ngày gần đây)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        # Quyên góp theo ngày trong 30 ngày qua
        daily_donations = Donation.objects.filter(
            payment_status='completed', 
            created_at__gte=thirty_days_ago
        ).annotate(
            day=TruncDay('created_at')
        ).values('day').annotate(
            count=Count('id'),
            total=Sum('amount')
        ).order_by('day')
        
        context['daily_donations'] = daily_donations
        
        # Chiến dịch thành công nhất
        top_campaigns = Campaign.objects.annotate(
            donation_count=Count('donations', filter=Q(donations__payment_status='completed')),
            total_raised=Sum('donations__amount', filter=Q(donations__payment_status='completed'))
        ).order_by('-total_raised')[:5]
        
        context['top_campaigns'] = top_campaigns
        
        # Chiến dịch gần đây
        context['recent_campaigns'] = Campaign.objects.order_by('-created_at')[:5]
        
        # Quyên góp gần đây
        context['recent_donations'] = Donation.objects.filter(
            payment_status='completed'
        ).select_related('campaign', 'user').order_by('-created_at')[:10]
        
        return context
