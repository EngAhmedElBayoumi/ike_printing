# Generated by Django 4.2.6 on 2024-01-04 08:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("senior_unicorn", "0003_meeting_meeting_url"),
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
                (
                    "file",
                    models.FileField(
                        blank=True, null=True, upload_to="uploads/meetings"
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="meeting",
            name="upload_file",
        ),
        migrations.AddField(
            model_name="meeting",
            name="files",
            field=models.ManyToManyField(
                blank=True, null=True, to="senior_unicorn.upload_file"
            ),
        ),
    ]
