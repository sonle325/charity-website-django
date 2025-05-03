from django.urls import path
from . import views
from .dashboard import DashboardView

app_name = "core"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]
