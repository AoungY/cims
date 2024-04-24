from django.contrib import admin

from .models import GovernmentUser, IdentityCard, OrdinaryUser, Passport

# Register your models here.

admin.site.register(Passport)
admin.site.register(IdentityCard)
admin.site.register(OrdinaryUser)
admin.site.register(GovernmentUser)
