# Generated by Django 4.2.6 on 2024-01-06 07:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("call_expert", "0045_upload_file"),
    ]

    operations = [
        migrations.AlterField(
            model_name="call_expert",
            name="call_type",
            field=models.CharField(
                choices=[("professional", "professional"), ("normal", "normal")],
                default="normal",
                max_length=20,
            ),
        ),
    ]