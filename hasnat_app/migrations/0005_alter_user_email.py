# Generated by Django 5.1.1 on 2024-10-01 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hasnat_app', '0004_user_phone_number_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
