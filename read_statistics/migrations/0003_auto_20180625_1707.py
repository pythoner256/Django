# Generated by Django 2.0.5 on 2018-06-25 09:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('read_statistics', '0002_auto_20180518_1120'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ReadDetial',
            new_name='ReadDetail',
        ),
    ]
