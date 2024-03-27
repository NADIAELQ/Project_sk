# Generated by Django 4.2.10 on 2024-03-13 12:11

import django.contrib.auth.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('carrier', '0003_remove_carrier_is_active_remove_carrier_is_admin_and_more'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='carrier',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='carrier',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined'),
        ),
        migrations.AddField(
            model_name='carrier',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
        migrations.AddField(
            model_name='carrier',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='carrier_groups', to='auth.group', verbose_name='Groups'),
        ),
        migrations.AddField(
            model_name='carrier',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='carrier',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='carrier',
            name='is_staff',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='carrier',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='carrier',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='carrier',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
        migrations.AddField(
            model_name='carrier',
            name='password',
            field=models.CharField(blank=True, default='', max_length=128, null=True, verbose_name='Password'),
        ),
        migrations.AddField(
            model_name='carrier',
            name='password_reset_token',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='carrier',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, related_name='carrier_permissions', to='auth.permission', verbose_name='User permissions'),
        ),
        migrations.AlterField(
            model_name='carrier',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='Business email'),
        ),
    ]
