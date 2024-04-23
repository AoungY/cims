from django.contrib import admin

# Register your models here.

from .models import Passport,IdentityCard

admin.site.register(Passport)
admin.site.register(IdentityCard)
