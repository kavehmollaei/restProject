from django.contrib import admin
from .models import User,Profile
from django.contrib.auth.admin import UserAdmin

# Register your models here.




class CustomUserAdmin(UserAdmin):
    model= User
    list_display = ['email','is_superuser','is_active','last_login']
    list_filter = ('email','is_superuser','is_active')
    search_fields = ['email']
    ordering = ('email',)
    readonly_fields = ('last_login',)
    fieldsets = ( 
        ('Authentication',{
        'fields':('email','password'),
        }),
         ("Group Permissions", {"fields": ["is_staff","is_active"]}),
    
    ('Important dates', {
            'fields': ('last_login',),  # Added last_login and date_joined
        }),
    )
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "password1","password2" ,"is_staff","is_active"],
            },
        ),
    ]
    
admin.site.register(User,CustomUserAdmin)
admin.site.register(Profile)
