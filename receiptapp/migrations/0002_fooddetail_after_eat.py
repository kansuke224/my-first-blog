# Generated by Django 2.2.5 on 2020-02-17 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receiptapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fooddetail',
            name='after_eat',
            field=models.BooleanField(default=False),
        ),
    ]
