# Generated by Django 2.0.7 on 2019-06-01 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20190601_1738'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='user_from',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='user_to',
        ),
        migrations.DeleteModel(
            name='Contact',
        ),
    ]
