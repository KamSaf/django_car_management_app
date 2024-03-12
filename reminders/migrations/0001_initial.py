# Generated by Django 5.0.1 on 2024-03-12 15:32

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cars', '0004_alter_car_num_plate'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.TextField(choices=[('service', 'Service'), ('fuel', 'Fuel'), ('others', 'Others')])),
                ('date', models.DateTimeField()),
                ('place', models.TextField(blank=True, max_length=200)),
                ('details', models.TextField(blank=True, max_length=100)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_edit_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars.car')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]