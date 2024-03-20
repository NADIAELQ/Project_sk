# Generated by Django 4.2.10 on 2024-03-13 00:33

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("carrier", "0005_carrier_is_staff"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="carrier",
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name="carrier",
            name="date_joined",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="date joined"
            ),
        ),
        migrations.AddField(
            model_name="carrier",
            name="first_name",
            field=models.CharField(
                blank=True, max_length=150, verbose_name="first name"
            ),
        ),
        migrations.AddField(
            model_name="carrier",
            name="last_name",
            field=models.CharField(
                blank=True, max_length=150, verbose_name="last name"
            ),
        ),
        migrations.AddField(
            model_name="carrier",
            name="username",
            field=models.CharField(
                default="",
                error_messages={"unique": "A user with that username already exists."},
                help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                max_length=150,
                unique=True,
                validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                verbose_name="username",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="carrier",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                related_name="carrier_groups",
                to="auth.group",
                verbose_name="Groups",
            ),
        ),
        migrations.AlterField(
            model_name="carrier",
            name="is_superuser",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="carrier",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                related_name="carrier_permissions",
                to="auth.permission",
                verbose_name="User permissions",
            ),
        ),
    ]
