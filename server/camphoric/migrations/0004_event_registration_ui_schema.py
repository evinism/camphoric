# Generated by Django 3.0 on 2020-01-05 04:10

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('camphoric', '0003_auto_20200104_2042'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='registration_ui_schema',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
    ]