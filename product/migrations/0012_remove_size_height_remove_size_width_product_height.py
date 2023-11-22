# Generated by Django 4.2.6 on 2023-11-21 13:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0011_remove_product_height_remove_product_price_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="size",
            name="height",
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
