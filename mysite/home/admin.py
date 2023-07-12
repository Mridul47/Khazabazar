from django.contrib import admin

# contact us ko form models.py ma banako kura eta import garya
from home.models import Contact, Profile, Dish, Order

# Register your models here.
admin.site.site_header="khazabazar | Admin"

class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'subject', 'added_on', 'is_approved']

class DishAdmin(admin.ModelAdmin):
    list_display = ['id','name','price','added_on','updated_on']

admin.site.register(Contact, ContactAdmin)
admin.site.register(Dish, DishAdmin )
admin.site.register(Profile)
admin.site.register(Order)