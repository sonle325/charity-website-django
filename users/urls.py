from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("profile/", views.UserProfileView.as_view(), name="profile"),
    path("profile/update/", views.UserProfileUpdateView.as_view(), name="profile_update"),
    path("demo-login/", views.demo_login_view, name="demo_login"), # Add URL for demo login
]


