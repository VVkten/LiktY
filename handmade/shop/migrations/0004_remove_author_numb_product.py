# Generated by Django 5.1.2 on 2024-10-28 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_rename_sellerform_seller'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='numb_product',
        ),
    ]