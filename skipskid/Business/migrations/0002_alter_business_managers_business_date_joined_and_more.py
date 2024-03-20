# Generated by Django 4.2.10 on 2024-03-20 13:10

import django.contrib.auth.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("Business", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="business",
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name="business",
            name="date_joined",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="date joined"
            ),
        ),
        migrations.AddField(
            model_name="business",
            name="email",
            field=models.EmailField(
                blank=True, max_length=254, verbose_name="email address"
            ),
        ),
        migrations.AddField(
            model_name="business",
            name="first_name",
            field=models.CharField(
                blank=True, max_length=150, verbose_name="first name"
            ),
        ),
        migrations.AddField(
            model_name="business",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                related_name="business_groups",
                related_query_name="business",
                to="auth.group",
                verbose_name="groups",
            ),
        ),
        migrations.AddField(
            model_name="business",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="business",
            name="is_admin",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="business",
            name="is_staff",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="business",
            name="is_superuser",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="business",
            name="last_login",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="last login"
            ),
        ),
        migrations.AddField(
            model_name="business",
            name="last_name",
            field=models.CharField(
                blank=True, max_length=150, verbose_name="last name"
            ),
        ),
        migrations.AddField(
            model_name="business",
            name="password",
            field=models.CharField(
                blank=True,
                default="",
                max_length=128,
                null=True,
                verbose_name="Password",
            ),
        ),
        migrations.AddField(
            model_name="business",
            name="password_reset_token",
            field=models.CharField(blank=True, default="", max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="business",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                related_name="business_user_permissions",
                related_query_name="business",
                to="auth.permission",
                verbose_name="user permissions",
            ),
        ),
    ]
