# Generated by Django 5.0.3 on 2024-03-08 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.CharField(default='', max_length=60),
        ),
    ]
