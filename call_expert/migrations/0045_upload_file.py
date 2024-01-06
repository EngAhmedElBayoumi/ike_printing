# Generated by Django 4.2.6 on 2024-01-06 06:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("call_expert", "0044_alter_call_expert_call_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="upload_file",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file", models.FileField(upload_to="files/")),
            ],
        ),
    ]
