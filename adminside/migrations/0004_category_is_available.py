# Generated by Django 4.2.3 on 2023-11-16 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0003_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]
