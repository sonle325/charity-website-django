from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from .models import Campaign, CampaignUpdate
from .forms import CampaignForm, CampaignUpdateForm

class StaffRequiredMixin(UserPassesTestMixin):
    """Mixin to require user to be staff."""
    def test_func(self):
        return self.request.user.is_staff

class CampaignListView(ListView):
    """View for listing all active campaigns."""
    model = Campaign
    template_name = "campaigns/list.html"
    context_object_name = "campaigns"
    queryset = Campaign.objects.filter(status="active").order_by("-created_at")
    paginate_by = 9 # Show 9 campaigns per page

class CampaignDetailView(DetailView):
    """View for displaying a single campaign."""
    model = Campaign
    template_name = "campaigns/detail.html"
    context_object_name = "campaign"
    slug_field = "slug"
    slug_url_kwarg = "slug" # Use slug in URL instead of pk

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campaign = self.get_object()
        context["updates"] = campaign.updates.all().order_by("-created_at")[:5] # Get latest 5 updates
        context["recent_donations"] = campaign.donations.filter(payment_status="completed").order_by("-created_at")[:10] # Get latest 10 donations
        return context

class CampaignCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    """View for creating a new campaign (staff only)."""
    model = Campaign
    form_class = CampaignForm
    template_name = "campaigns/campaign_form.html"
    success_url = reverse_lazy("campaigns:list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, _("Chiến dịch đã được tạo thành công."))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = _("Tạo Chiến Dịch Mới")
        return context

class CampaignUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    """View for updating an existing campaign (staff only)."""
    model = Campaign
    form_class = CampaignForm
    template_name = "campaigns/campaign_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_success_url(self):
        return reverse_lazy("campaigns:detail", kwargs={"slug": self.object.slug})

    def form_valid(self, form):
        messages.success(self.request, _("Chiến dịch đã được cập nhật thành công."))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = _("Cập Nhật Chiến Dịch")
        return context

class CampaignUpdateCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    """View for creating a new campaign update (staff only)."""
    model = CampaignUpdate
    form_class = CampaignUpdateForm
    template_name = "campaigns/campaign_update_form.html"

    def form_valid(self, form):
        self.campaign = get_object_or_404(Campaign, slug=self.kwargs["campaign_slug"])
        form.instance.campaign = self.campaign
        form.instance.created_by = self.request.user
        messages.success(self.request, _("Cập nhật chiến dịch đã được thêm thành công."))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("campaigns:detail", kwargs={"slug": self.kwargs["campaign_slug"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["campaign"] = get_object_or_404(Campaign, slug=self.kwargs["campaign_slug"])
        context["form_title"] = _("Thêm Cập Nhật Cho Chiến Dịch")
        return context
