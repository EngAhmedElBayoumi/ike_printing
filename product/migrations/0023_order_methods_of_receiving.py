# Generated by Django 4.2.6 on 2023-12-05 05:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0022_remove_cartproduct_user_order_cartproduct_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="methods_of_receiving",
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
