# Generated by Django 5.0.7 on 2024-08-12 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='petimage',
            field=models.ImageField(default=0, upload_to='media'),
        ),
    ]
