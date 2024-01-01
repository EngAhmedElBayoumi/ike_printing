from django.contrib import admin
from django.utils.html import format_html
from .models import ContactUs , ContactList


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'is_read_display', 'message_display']
    search_fields = ['name', 'subject']
    def is_read_display(self, obj):
        if obj.is_read:
            return format_html('<strong>Read</strong>')
        else:
            return format_html('<strong style="color:red;">UnRead</strong>')
    is_read_display.short_description = 'Read Status'
    def message_display(self, obj):
        if not obj.is_read:
            return obj.message
        else:
            return obj.message


    message_display.short_description = 'Message'
    #firlter by is_read
    list_filter = ['is_read']

admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(ContactList)

