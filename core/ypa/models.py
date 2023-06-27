from django.db import models
from django.contrib.auth.models import User

class ApiKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    youtube_api_key= models.CharField(max_length=100, null=True, blank=True)
    openai_api_key = models.CharField(max_length=100, null=True, blank=True)
    huggingfacehub_api_key = models.CharField(max_length=100, null=True, blank=True)