# Generated by Django 3.1.2 on 2020-11-01 00:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20201031_1659'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='user',
            new_name='author',
        ),
    ]