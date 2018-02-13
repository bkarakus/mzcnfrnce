
from django.contrib import admin

from .models import EmailTemplate, EmailLog

class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'subject', 'visible_from_address')
    search_fields = ('title', 'slug', 'subject', 'from_address', 'body')
    fieldsets = (
        (None, {'fields': ('title', 'slug', 'from_address')}),
        ('Email', {'fields': ('subject', 'txt_body',)}),
    )
    prepopulated_fields = {'slug': ('title',)}
    
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('from_email', 'recipients', 'subject', 'ok', 'date_sent')
    readonly_fields = ('from_email', 'recipients', 'subject', 'body', 'ok', 'date_sent')
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
admin.site.register(EmailTemplate, EmailTemplateAdmin)
admin.site.register(EmailLog, EmailLogAdmin)