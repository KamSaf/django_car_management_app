# Generated by Django 5.0.1 on 2024-03-09 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0004_rename_notes_entry_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='details',
            field=models.TextField(blank=True, max_length=1024),
        ),
        migrations.AlterField(
            model_name='entry',
            name='place',
            field=models.TextField(blank=True, max_length=200),
        ),
    ]
