from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account

class AccountAdmin(UserAdmin):
    list_display = ('email', 'full_name', 'username', 'last_login', 'is_staff', 'is_admin', 'date_joined')
    search_fields = ('email', 'username', 'full_name')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter =()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)
