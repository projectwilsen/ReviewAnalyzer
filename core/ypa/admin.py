from django.contrib import admin
from .models import User, ApiKey, Result

# Register your models here.
admin.site.register(ApiKey)
admin.site.register(Result)