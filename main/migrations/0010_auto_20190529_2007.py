# Generated by Django 2.0.7 on 2019-05-29 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_vote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='user',
        ),
        migrations.DeleteModel(
            name='Vote',
        ),
    ]
