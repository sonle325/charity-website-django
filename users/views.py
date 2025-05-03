from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate

from .models import CustomUser
from .forms import UserProfileForm

class UserProfileView(LoginRequiredMixin, DetailView):
    """View for displaying user profile information."""
    model = CustomUser
    template_name = 'users/profile.html'
    context_object_name = 'user'
    
    def get_object(self):
        return self.request.user

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating user profile information."""
    model = CustomUser
    form_class = UserProfileForm
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('users:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, _('Your profile has been updated successfully.'))
        return super().form_valid(form)

def demo_login_view(request):
    """Logs in the demo user automatically."""
    try:
        # Use authenticate to check if the user exists and is active, 
        # even though we won't use the password here for login.
        # This helps prevent errors if the demo user somehow gets deleted or deactivated.
        user = authenticate(request, email='demo@example.com', password='demopassword123')
        if user is not None:
            login(request, user)
            messages.success(request, _('Successfully logged in as demo user.'))
            return redirect('core:home')
        else:
            # Handle case where demo user doesn't exist or is inactive
            messages.error(request, _('Demo user account not found or inactive.'))
            return redirect('account_login') # Redirect back to login page
    except CustomUser.DoesNotExist:
        messages.error(request, _('Demo user account does not exist.'))
        return redirect('account_login') # Redirect back to login page
    except Exception as e:
        messages.error(request, _('An error occurred during demo login: {}').format(e))
        return redirect('account_login') # Redirect back to login page

