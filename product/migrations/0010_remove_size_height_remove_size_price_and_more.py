# Generated by Django 4.2.6 on 2023-11-21 01:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0009_size_height_size_width"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="size",
            name="height",
        ),
        migrations.RemoveField(
            model_name="size",
            name="price",
        ),
        migrations.RemoveField(
            model_name="size",
            name="width",
        ),
        migrations.AddField(
            model_name="product",
            name="height",
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]