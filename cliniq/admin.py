from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from cliniq.models import *
# Register your models here.
from .forms import UserCreationForm, UserChangeForm






admin.site.register(CliniqUser)


admin.site.site_header = 'clinic Admin'



admin.site.register(Patient)

admin.site.register(RDV)
