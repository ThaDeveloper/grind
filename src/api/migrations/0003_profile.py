# Generated by Django 2.2.4 on 2019-11-04 08:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20191101_1148'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('title', models.CharField(blank=True, max_length=30)),
                ('bio', models.TextField(blank=True)),
                ('profile_picture', models.URLField(blank=True)),
                ('phone', models.CharField(blank=True, max_length=30)),
                ('location', models.CharField(blank=True, max_length=30)),
                ('address_1', models.CharField(blank=True, max_length=200)),
                ('address_2', models.CharField(blank=True, max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
                'ordering': ('pk',),
            },
        ),
    ]
