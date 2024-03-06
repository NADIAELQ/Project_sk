# Generated by Django 4.2.10 on 2024-03-03 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0005_alter_delivery_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='')),
                ('delivery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='delivery.delivery')),
            ],
        ),
    ]