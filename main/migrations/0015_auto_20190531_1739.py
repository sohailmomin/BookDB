# Generated by Django 2.0.7 on 2019-05-31 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_book_amazon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='amazon',
            field=models.URLField(default='https://www.amazon.com/', max_length=400),
        ),
    ]
