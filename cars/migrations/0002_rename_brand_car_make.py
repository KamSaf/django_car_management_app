# Generated by Django 5.0.1 on 2024-03-05 13:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='car',
            old_name='brand',
            new_name='make',
        ),
    ]