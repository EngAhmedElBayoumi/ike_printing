# Generated by Django 4.2.6 on 2023-12-02 13:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("call_expert", "0026_alter_call_expert_call_type"),
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
