# Generated by Django 2.0.7 on 2019-05-29 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20190528_1700'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
