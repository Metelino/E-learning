# Generated by Django 3.1.3 on 2021-05-19 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_auto_20210519_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.CharField(choices=[('other', 'inna'), ('infa', 'informatyka'), ('matma', 'matematyka'), ('fizyka', 'fizyka'), ('biologia', 'biologia'), ('chemia', 'chemia')], default='other', max_length=100),
        ),
    ]
