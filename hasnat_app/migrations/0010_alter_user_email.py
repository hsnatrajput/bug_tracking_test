# Generated by Django 5.1.1 on 2024-10-01 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hasnat_app', '0009_auto_20241001_0634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]
