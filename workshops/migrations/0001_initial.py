# Generated by Django 5.0.1 on 2024-02-23 14:05

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=100)),
                ('city', models.TextField(blank=True, max_length=100)),
                ('street', models.TextField(blank=True, max_length=100)),
                ('phone_number', models.TextField(blank=True, max_length=9)),
                ('profession', models.TextField(blank=True, max_length=100)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('favourite', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
