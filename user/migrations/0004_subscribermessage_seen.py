# Generated by Django 3.0.3 on 2020-02-13 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20200213_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscribermessage',
            name='seen',
            field=models.BooleanField(default=False),
        ),
    ]