# Generated by Django 2.0.7 on 2019-05-29 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20190529_2024'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='votes',
            field=models.IntegerField(default=0),
        ),
    ]