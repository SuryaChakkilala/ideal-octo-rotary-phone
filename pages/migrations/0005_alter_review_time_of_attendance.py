# Generated by Django 4.1.6 on 2023-03-31 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0004_review_time_of_attendance"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="time_of_attendance",
            field=models.TimeField(null=True),
        ),
    ]
