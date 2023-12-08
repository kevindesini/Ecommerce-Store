# Generated by Django 4.2.3 on 2023-12-05 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0010_rename_user_orderproduct_user_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Accepted', 'Accepted'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled'), ('Pending', 'Pending')], default='New', max_length=10),
        ),
    ]
