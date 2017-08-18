# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-16 20:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0002_account'),
    ]

    operations = [
        migrations.CreateModel(
            name='SynapseUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('synapse_id', models.CharField(max_length=255)),
                ('refresh_token', models.CharField(max_length=255)),
                ('covered_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]