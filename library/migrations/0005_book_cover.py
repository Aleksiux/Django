# Generated by Django 4.2 on 2023-05-03 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_author_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover',
            field=models.ImageField(null=True, upload_to='covers', verbose_name='Cover'),
        ),
    ]
