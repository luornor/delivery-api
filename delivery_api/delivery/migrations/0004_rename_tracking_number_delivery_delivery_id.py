# Generated by Django 5.0.7 on 2024-07-16 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0003_delivery_delivery_method_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='delivery',
            old_name='tracking_number',
            new_name='delivery_id',
        ),
    ]
