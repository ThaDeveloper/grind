# Generated by Django 2.2.4 on 2019-11-04 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='profile_picture',
            new_name='image',
        ),
    ]