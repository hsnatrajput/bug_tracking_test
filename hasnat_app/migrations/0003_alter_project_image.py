# Generated by Django 5.1.1 on 2024-09-27 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hasnat_app', '0002_remove_bug_screenshot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='image',
            field=models.ImageField(upload_to='media/project_pic/'),
        ),
    ]