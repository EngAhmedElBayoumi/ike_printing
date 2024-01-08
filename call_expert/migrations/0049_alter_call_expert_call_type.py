# Generated by Django 4.2.6 on 2024-01-06 22:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("call_expert", "0048_merge_20240107_0029"),
    ]

    operations = [
        migrations.AlterField(
            model_name="call_expert",
            name="call_type",
            field=models.CharField(
                choices=[("normal", "normal"), ("professional", "professional")],
                default="normal",
                max_length=20,
            ),
        ),
    ]