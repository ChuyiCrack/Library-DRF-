# Generated by Django 5.0.3 on 2024-03-18 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0006_book_existence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='description',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
