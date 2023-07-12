# Generated by Django 4.2.2 on 2023-07-11 14:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ypa', '0003_delete_result'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('videoid', models.CharField(blank=True, max_length=20, null=True)),
                ('videotitle', models.CharField(blank=True, max_length=200, null=True)),
                ('view', models.CharField(blank=True, max_length=20, null=True)),
                ('like', models.CharField(blank=True, max_length=10, null=True)),
                ('comment', models.CharField(blank=True, max_length=10, null=True)),
                ('total_positive_comment', models.CharField(blank=True, max_length=10, null=True)),
                ('positive_comment', models.CharField(blank=True, max_length=5000, null=True)),
                ('total_negative_comment', models.CharField(blank=True, max_length=10, null=True)),
                ('negative_comment', models.CharField(blank=True, max_length=5000, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
