from django.contrib import admin
from .models import Campaign, CampaignUpdate

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'target_amount', 'current_amount', 'progress_percentage', 'start_date', 'end_date', 'created_at')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('title', 'description', 'short_description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('current_amount', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'short_description', 'image')
        }),
        ('Thông tin tài chính', {
            'fields': ('target_amount', 'current_amount')
        }),
        ('Thời gian', {
            'fields': ('start_date', 'end_date')
        }),
        ('Trạng thái', {
            'fields': ('status', 'created_by', 'created_at', 'updated_at')
        }),
    )

@admin.register(CampaignUpdate)
class CampaignUpdateAdmin(admin.ModelAdmin):
    list_display = ('title', 'campaign', 'created_at', 'created_by')
    list_filter = ('campaign', 'created_at')
    search_fields = ('title', 'content', 'campaign__title')
    readonly_fields = ('created_at',)
