from users.models import CustomUser
from allauth.account.models import EmailAddress
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

email = "demo@example.com"
password = "demopassword123"

# Check if user already exists
if CustomUser.objects.filter(email=email).exists():
    print(f"User with email {email} already exists.")
    user = CustomUser.objects.get(email=email)
    # Ensure the existing user's email is verified
    try:
        email_address = EmailAddress.objects.get(user=user, email=email)
        if not email_address.verified:
            email_address.verified = True
            email_address.save()
            print(f"Verified email for existing user: {email}")
        else:
            print(f"Email already verified for existing user: {email}")
    except EmailAddress.DoesNotExist:
        email_address = EmailAddress.objects.create(user=user, email=email, primary=True, verified=True)
        print(f"Created and verified email address for existing user: {email}")
else:
    # Create the user
    user = CustomUser.objects.create_user(email=email, password=password)
    user.is_active = True # Ensure user is active
    user.save()
    print(f"Created user: {email}")

    # Verify the email address
    try:
        email_address = EmailAddress.objects.get(user=user, email=email)
        if not email_address.verified:
            email_address.verified = True
            email_address.save()
            print(f"Verified email for user: {email}")
        else:
            print(f"Email already verified for user: {email}")
    except EmailAddress.DoesNotExist:
        # If EmailAddress object wasn't created automatically
        email_address = EmailAddress.objects.create(user=user, email=email, primary=True, verified=True)
        print(f"Created and verified email address for user: {email}")

print(f"\nDemo User Credentials:")
print(f"Email: {email}")
print(f"Password: {password}")

