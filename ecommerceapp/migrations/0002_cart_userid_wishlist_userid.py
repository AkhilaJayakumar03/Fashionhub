# Generated by Django 4.1.5 on 2023-02-21 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='userid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wishlist',
            name='userid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
