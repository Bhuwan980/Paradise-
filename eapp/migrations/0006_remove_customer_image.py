# Generated by Django 3.2.4 on 2021-06-18 03:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eapp', '0005_customer_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='image',
        ),
    ]