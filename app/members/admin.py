from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from members.models import User

# user의 model정보를 fieldsets 형식으로 저장
# fieldsets = ((None, {'fields':(username','password',)})
# ('개인정보', {'fields':('last_name', 'first_name'...)})
# fields에 개인정보 안에 fields:('last_name', 'first_name')의 형식
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {
          'fields': (
              'username',
              'password',
          ),
        }),
        ('개인정보', {
            'fields': (
                'last_name',
                'first_name',
                'gender',
                'email',
                'img_profile',
                'introduce',
                'site',
             ),
        }),
        ('권한', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
        ('주요 일자', {
            'fields': (
                'last_login',
                'date_joined',
            ),
        }),
    )

admin.site.register(User, UserAdmin)
