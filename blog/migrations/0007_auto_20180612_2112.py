# Generated by Django 2.0.5 on 2018-06-12 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20180517_1814'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogtype',
            options={'ordering': ['-type_name']},
        ),
    ]
