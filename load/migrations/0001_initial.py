# Generated by Django 2.0.13 on 2019-04-02 03:15

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Load',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickup_date', models.DateField(default=datetime.datetime(2019, 4, 2, 0, 15, 24, 16746))),
                ('ref', models.CharField(max_length=200)),
                ('origin_city', models.CharField(max_length=200)),
                ('destination_city', models.CharField(max_length=200)),
                ('price', models.FloatField()),
                ('carrier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='carrier', to=settings.AUTH_USER_MODEL)),
                ('shipper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shipper', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]