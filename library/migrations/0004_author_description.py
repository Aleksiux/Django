# Generated by Django 4.2 on 2023-04-27 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_alter_book_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='description',
            field=models.TextField(default='', help_text='Enter author description:', max_length=1000, verbose_name='Description'),
        ),
    ]
