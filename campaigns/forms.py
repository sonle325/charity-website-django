from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Campaign, CampaignUpdate

class CampaignForm(forms.ModelForm):
    """Form for creating and updating campaigns."""
    class Meta:
        model = Campaign
        fields = ['title', 'short_description', 'description', 'target_amount', 
                  'start_date', 'end_date', 'image', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'target_amount': forms.NumberInput(attrs={'class': 'form-control', 'min': '1000000'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': _('Tiêu đề chiến dịch'),
            'short_description': _('Mô tả ngắn'),
            'description': _('Mô tả chi tiết'),
            'target_amount': _('Số tiền mục tiêu (VNĐ)'),
            'start_date': _('Ngày bắt đầu'),
            'end_date': _('Ngày kết thúc'),
            'image': _('Hình ảnh chiến dịch'),
            'status': _('Trạng thái'),
        }

class CampaignUpdateForm(forms.ModelForm):
    """Form for creating campaign updates."""
    class Meta:
        model = CampaignUpdate
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
        labels = {
            'title': _('Tiêu đề cập nhật'),
            'content': _('Nội dung cập nhật'),
            'image': _('Hình ảnh (tùy chọn)'),
        }
