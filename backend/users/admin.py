from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from users.models import Balance, CustomUser, Purchase


@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'role'), },),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('username', 'usable_password', 'password1', 'password2', 'role'), },),
    )
    list_display = ('id', 'email', 'username', 'first_name', 'last_name', 'role', 'get_user_balance')
    list_filter = ('role',)
    search_fields = ('username', 'first_name', 'last_name', 'email')
    filter_horizontal = ('user_permissions',)

    @admin.display(description='Баланс')
    def get_user_balance(self, obj):
        return obj.balance.amount


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'purchased_at')

    def save_model(self, request, obj, form, change):
        try:
            Purchase.objects.create_purchase(user=obj.user, course=obj.course)
        except ValidationError as e:
            raise ValidationError(f'Ошибка: {e}.')

    def delete_model(self, request, obj):
        try:
            Purchase.objects.delete_purchase(user=obj.user, course=obj.course)
        except ValidationError as e:
            raise ValidationError(f'Ошибка: {e}.')


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount')


admin.site.unregister(Group)
