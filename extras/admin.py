from django.contrib import admin
from .models import Address, Extras

# Register your models here.
admin.site.register(Extras)
admin.site.register(Address)