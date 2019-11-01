# Generated by Django 2.2.4 on 2019-11-01 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('profile_picture', models.CharField(max_length=500, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('title', models.CharField(max_length=30, null=True)),
                ('phone', models.CharField(max_length=30, null=True)),
                ('location', models.CharField(max_length=30, null=True)),
                ('address_1', models.CharField(max_length=200, null=True)),
                ('address_2', models.CharField(max_length=200, null=True)),
                ('active', models.BooleanField(default=True)),
                ('admin', models.BooleanField(default=False)),
                ('staff', models.BooleanField(default=False)),
                ('user_type', models.CharField(choices=[('professional', 'professional'), ('client', 'client')], max_length=20)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'ordering': ('pk',),
            },
        ),
    ]
