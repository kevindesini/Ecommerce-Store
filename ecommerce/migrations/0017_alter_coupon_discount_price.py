# Generated by Django 4.2.3 on 2023-12-12 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0016_alter_coupon_discount_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='discount_price',
            field=models.IntegerField(default=100),
        ),
    ]
