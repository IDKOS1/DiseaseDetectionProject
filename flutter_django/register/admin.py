from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User
from django.utils.translation import gettext_lazy as _


class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'birth', 'gender', 'number', 'farm')


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (_('Account'), {'fields': ('email', 'password')}),
        (_('Info'), {'fields': ('username', 'birth', 'gender', 'number', 'farm')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('email', 'username', 'birth', 'gender', 'number', 'farm', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'username')
    ordering = ('email',)


admin.site.register(User, MyUserAdmin)
