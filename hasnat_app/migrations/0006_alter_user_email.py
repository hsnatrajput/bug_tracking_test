# Generated by Django 5.1.1 on 2024-10-01 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hasnat_app', '0005_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
    ]
