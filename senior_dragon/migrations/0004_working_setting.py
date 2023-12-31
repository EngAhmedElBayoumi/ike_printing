# Generated by Django 4.2.6 on 2023-12-30 21:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("senior_dragon", "0003_delete_working_setting"),
    ]

    operations = [
        migrations.CreateModel(
            name="working_setting",
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
                    "day",
                    models.CharField(
                        choices=[
                            ("Monday", "Monday"),
                            ("Tuesday", "Tuesday"),
                            ("Wednesday", "Wednesday"),
                            ("Thursday", "Thursday"),
                            ("Friday", "Friday"),
                            ("Saturday", "Saturday"),
                            ("Sunday", "Sunday"),
                        ],
                        max_length=10,
                    ),
                ),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                ("meeting_duration_hour", models.IntegerField(blank=True, null=True)),
                ("meeting_duration_minute", models.IntegerField(blank=True, null=True)),
                ("break_time_from", models.TimeField()),
                ("break_time_to", models.TimeField()),
                ("meeting_price", models.IntegerField()),
            ],
        ),
    ]