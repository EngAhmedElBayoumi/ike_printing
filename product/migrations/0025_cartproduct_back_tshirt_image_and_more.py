# Generated by Django 4.2.6 on 2023-12-09 06:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0024_alter_order_methods_of_receiving"),
    ]

    operations = [
        migrations.AddField(
            model_name="cartproduct",
            name="back_tshirt_image",
            field=models.ImageField(
                blank=True, null=True, upload_to="product/cartproduct_image"
            ),
        ),
        migrations.AddField(
            model_name="cartproduct",
            name="front_tshirt_image",
            field=models.ImageField(
                blank=True, null=True, upload_to="product/cartproduct_image"
            ),
        ),
    ]