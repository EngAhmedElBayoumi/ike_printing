# Generated by Django 4.2.6 on 2024-01-02 18:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("call_expert", "0032_alter_call_expert_call_type"),
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
