# Generated by Django 4.2.6 on 2023-11-07 13:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="city",
        ),
        migrations.AlterField(
            model_name="profile",
            name="country",
            field=models.CharField(
                blank=True, choices=[("US", "United States")], max_length=2
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="users/profile_image"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="state",
            field=models.CharField(
                blank=True,
                choices=[
                    ("AL", "Alabama"),
                    ("AK", "Alaska"),
                    ("AZ", "Arizona"),
                    ("AR", "Arkansas"),
                    ("CA", "California"),
                    ("CO", "Colorado"),
                    ("CT", "Connecticut"),
                    ("DE", "Delaware"),
                    ("DC", "District Of Columbia"),
                    ("FL", "Florida"),
                    ("GA", "Georgia"),
                    ("HI", "Hawaii"),
                    ("ID", "Idaho"),
                    ("IL", "Illinois"),
                    ("IN", "Indiana"),
                    ("IA", "Iowa"),
                    ("KS", "Kansas"),
                    ("KY", "Kentucky"),
                    ("LA", "Louisiana"),
                    ("ME", "Maine"),
                    ("MD", "Maryland"),
                    ("MA", "Massachusetts"),
                    ("MI", "Michigan"),
                    ("MN", "Minnesota"),
                    ("MS", "Mississippi"),
                    ("MO", "Missouri"),
                    ("MT", "Montana"),
                    ("NE", "Nebraska"),
                    ("NV", "Nevada"),
                    ("NH", "New Hampshire"),
                    ("NJ", "New Jersey"),
                    ("NM", "New Mexico"),
                    ("NY", "New York"),
                    ("NC", "North Carolina"),
                    ("ND", "North Dakota"),
                    ("OH", "Ohio"),
                    ("OK", "Oklahoma"),
                    ("OR", "Oregon"),
                    ("PA", "Pennsylvania"),
                    ("RI", "Rhode Island"),
                    ("SC", "South Carolina"),
                    ("SD", "South Dakota"),
                    ("TN", "Tennessee"),
                    ("TX", "Texas"),
                    ("UT", "Utah"),
                    ("VT", "Vermont"),
                    ("VA", "Virginia"),
                    ("WA", "Washington"),
                    ("WV", "West Virginia"),
                    ("WI", "Wisconsin"),
                    ("WY", "Wyoming"),
                ],
                max_length=2,
            ),
        ),
    ]
