# Generated by Django 2.0.7 on 2018-07-06 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('strl_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='world',
            old_name='owner_id',
            new_name='owner',
        ),
    ]
