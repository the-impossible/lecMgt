# Generated by Django 4.2.1 on 2023-06-03 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lecMgt_auth", "0004_user_department"),
    ]

    operations = [
        migrations.AlterField(
            model_name="department",
            name="dept_title",
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
