# Generated by Django 4.1.6 on 2023-03-31 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0007_remove_student_posted_by"),
    ]

    operations = [
        migrations.RemoveField(model_name="student", name="contact_no",),
        migrations.RemoveField(model_name="student", name="email",),
    ]
