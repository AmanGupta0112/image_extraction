# Generated by Django 5.0.3 on 2024-03-04 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extract', '0002_alter_filemanager_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filemanager',
            name='file',
            field=models.ImageField(upload_to=''),
        ),
    ]
