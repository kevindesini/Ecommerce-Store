# Generated by Django 4.2.3 on 2023-11-20 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0006_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to='photos/products'),
        ),
    ]
