# Generated by Django 4.2.10 on 2024-03-06 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipper', '0002_individual_business'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='individual',
            name='shipper',
        ),
        migrations.DeleteModel(
            name='Business',
        ),
        migrations.DeleteModel(
            name='Individual',
        ),
    ]