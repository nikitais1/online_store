# Generated by Django 4.2 on 2024-02-09 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_alter_product_is_published'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Blog',
        ),
    ]
