# Generated by Django 3.1.3 on 2021-03-27 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20210327_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, null=True),
        ),
    ]
