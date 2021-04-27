# Generated by Django 3.1.3 on 2021-04-22 09:03

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_auto_20210422_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonfile',
            name='lesson_type',
            field=models.CharField(choices=[('0', 'Wzrokowiec'), ('1', 'Kinestetyk'), ('2', 'Słuchowiec')], default='0', max_length=20, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message=None)]),
        ),
    ]
