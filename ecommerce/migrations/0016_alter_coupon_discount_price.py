# Generated by Django 4.2.3 on 2023-12-09 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0015_alter_coupon_discount_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='discount_price',
            field=models.IntegerField(default=100, null=True),
        ),
    ]