from django.contrib import admin
from .models import AuthUser

class PersonAdmin(admin.ModelAdmin):
    exclude = ('email', 'date_joined', )

admin.site.register(AuthUser, PersonAdmin)
    