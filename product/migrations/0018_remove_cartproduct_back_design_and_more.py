# Generated by Django 4.2.6 on 2023-11-30 04:57

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0017_cartproduct_back_design_cartproduct_front_design"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cartproduct",
            name="back_design",
        ),
        migrations.RemoveField(
            model_name="cartproduct",
            name="front_design",
        ),
    ]
