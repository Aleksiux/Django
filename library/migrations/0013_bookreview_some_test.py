# Generated by Django 4.2 on 2023-05-15 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0012_merge_20230515_2106'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookreview',
            name='some_test',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
    ]
