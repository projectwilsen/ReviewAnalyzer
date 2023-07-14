from django.db import models
from django.contrib.auth.models import User

class ApiKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    youtube_api_key= models.CharField(max_length=100, null=True, blank=True)
    openai_api_key = models.CharField(max_length=100, null=True, blank=True)
    huggingfacehub_api_key = models.CharField(max_length=100, null=True, blank=True)

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    videoid= models.CharField(max_length=20, null=True, blank=True)
    videotitle= models.CharField(max_length=200, null=True, blank=True)
    view = models.CharField(max_length=20, null=True, blank=True)
    like = models.CharField(max_length=10, null=True, blank=True)
    comment = models.CharField(max_length=10, null=True, blank=True)
    total_positive_comment = models.CharField(max_length=10, null=True, blank=True)
    positive_comment = models.CharField(max_length=5000, null=True, blank=True)
    total_negative_comment = models.CharField(max_length=10, null=True, blank=True)
    negative_comment = models.CharField(max_length=5000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.videoid