from django.contrib import admin

# contact us ko form models.py ma banako kura eta import garya
from home.models import Contact

# Register your models here.
admin.site.site_header="khazabazar | Admin"

class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'subject', 'added_on', 'is_approved']

admin.site.register(Contact, ContactAdmin)