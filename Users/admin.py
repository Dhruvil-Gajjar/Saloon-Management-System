from django.contrib import admin
from Users.models import Users


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_customer', 'is_employee', 'is_superuser')


admin.site.register(Users, UserAdmin)
