# Generated by Django 4.1.2 on 2022-11-16 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0005_passwords_custom_fields"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="passwords",
            name="custom_fields",
        ),
        migrations.RemoveField(
            model_name="passwords",
            name="password",
        ),
        migrations.AddField(
            model_name="passwords",
            name="fields",
            field=models.TextField(null=True),
        ),
    ]
