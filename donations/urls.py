from django.urls import path
from . import views

app_name = "donations"

urlpatterns = [
    path("donate/<int:campaign_id>/", views.CreateDonationView.as_view(), name="create"),
    # path("success/<int:donation_id>/", views.DonationSuccessView.as_view(), name="success"),
    path("history/", views.DonationHistoryView.as_view(), name="history"),
    path("now/", views.donation_now_view, name="donation_now"),
    path("confirm/<int:pk>/", views.DonationConfirmView.as_view(), name="donation_confirm"),
    
    # Demo QR Code Display URL
    # path("qr-display-demo/<int:donation_id>/", views.QRDisplayDemoView.as_view(), name="qr_display_demo"),
    path("qr/<int:donation_id>/", views.donation_qr_code_page, name="qr_code"),
    
    # Payment Return URL (used by demo confirmation)
    # path("payment-return/", views.PaymentReturnView.as_view(), name="payment_return"), 
    
    # Reporting URL (Staff Only)
    # path("report/", views.DonationReportView.as_view(), name="report"),
    
    # path("simulate-payment/<int:donation_id>/", views.SimulatePaymentView.as_view(), name="simulate_payment"), # Old simulation URL - commented out
]

