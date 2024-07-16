# Generated by Django 5.0.7 on 2024-07-15 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='current_location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='delivery',
            name='estimated_delivery_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='status',
            field=models.CharField(choices=[('on_hold', 'On Hold'), ('ready', 'Ready'), ('on_the_way', 'On the Way'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], default='on_hold', max_length=20),
        ),
    ]
