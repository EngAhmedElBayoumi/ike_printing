# Generated by Django 4.2.6 on 2023-11-25 22:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("unicorn", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="meeting",
            name="upload_file",
            field=models.FileField(blank=True, null=True, upload_to="uploads/meetings"),
        ),
    ]
