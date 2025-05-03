from django.urls import path
from . import views

app_name = "campaigns"

urlpatterns = [
    path("", views.CampaignListView.as_view(), name="list"),
    path("create/", views.CampaignCreateView.as_view(), name="create"),
    path("<slug:slug>/", views.CampaignDetailView.as_view(), name="detail"),
    path("<slug:slug>/edit/", views.CampaignUpdateView.as_view(), name="update"),
    path("<slug:campaign_slug>/updates/add/", views.CampaignUpdateCreateView.as_view(), name="add_update"),
]
