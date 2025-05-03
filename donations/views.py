import qrcode
import base64
from io import BytesIO
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Donation
from django.conf import settings
from django.http import HttpResponse
import urllib.parse

def donation_qr_code_page(request, donation_id):
    """Render a page displaying the QR code for a donation."""
    donation = get_object_or_404(Donation, id=donation_id)
    # Build VNPay payment URL or use existing payment URL for QR code data
    vnp_params = {
        'vnp_Version': '2.1.0',
        'vnp_Command': 'pay',
        'vnp_TmnCode': 'sandbox_tmn_code',  # Replace with your sandbox terminal code
        'vnp_Amount': str(int(donation.amount) * 100),  # Amount in smallest currency unit
        'vnp_CurrCode': 'VND',
        'vnp_TxnRef': str(donation.id),  # Unique transaction reference
        'vnp_OrderInfo': f'Donation payment for donation {donation.id}',
        'vnp_Locale': 'vn',
        'vnp_ReturnUrl': settings.PAYMENT_GATEWAY.get('RETURN_URL', ''),
        'vnp_IpAddr': request.META.get('REMOTE_ADDR', ''),
    }
    sorted_params = sorted(vnp_params.items())
    query_string = urllib.parse.urlencode(sorted_params)
    vnpay_url = f"https://sandbox.vnpayment.vn/paymentv2/vpcpay.html?{query_string}"

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(vnpay_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()

    context = {
        'donation': donation,
        'qr_code_base64': img_str,
        'vnpay_url': vnpay_url,
    }
    return render(request, 'donations/qr_code.html', context)

from django.http import JsonResponse

def donation_now_view(request):
    """Donation now page with VNPay sandbox QR code."""
    if request.GET.get('ajax') == '1':
        # Generate QR code and return JSON response for AJAX request
        vnp_params = {
            'vnp_Version': '2.1.0',
            'vnp_Command': 'pay',
            'vnp_TmnCode': 'sandbox_tmn_code',  # Replace with your sandbox terminal code
            'vnp_Amount': '1000000',  # Amount in smallest currency unit (e.g., 1000000 = 10000.00 VND)
            'vnp_CurrCode': 'VND',
            'vnp_TxnRef': '123456789',  # Unique transaction reference
            'vnp_OrderInfo': 'Donation payment',
            'vnp_Locale': 'vn',
            'vnp_ReturnUrl': settings.PAYMENT_GATEWAY.get('RETURN_URL', ''),
            'vnp_IpAddr': request.META.get('REMOTE_ADDR', ''),
        }
        sorted_params = sorted(vnp_params.items())
        query_string = urllib.parse.urlencode(sorted_params)
        vnpay_url = f"https://sandbox.vnpayment.vn/paymentv2/vpcpay.html?{query_string}"

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(vnpay_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()

        return JsonResponse({'vnpay_url': vnpay_url, 'qr_code_base64': img_str})

    # Normal GET request renders the page with button
    return render(request, 'donations/donation_now.html')

class CreateDonationView(CreateView):
    model = Donation
    fields = ['campaign', 'amount', 'donor_name', 'donor_email']  # Adjust fields as per your model
    template_name = 'donations/donation_form.html'

    def get_success_url(self):
        return reverse_lazy('donations:donation_confirm', kwargs={'pk': self.object.id})

from django.views.generic import DetailView

from django.views.generic import DetailView

class DonationConfirmView(DetailView):
    model = Donation
    template_name = 'donations/donation_confirm.html'
    context_object_name = 'donation'

class DonationHistoryView(ListView):
    model = Donation
    template_name = 'donations/history.html'
    context_object_name = 'donations'
