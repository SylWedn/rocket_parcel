# Generated by Django 4.2.6 on 2023-11-13 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0010_uploadfiles_alter_packagedb_is_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='packagedb',
            name='photo',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='photos/%Y/%m/%d/', verbose_name='Photo'),
        ),
    ]