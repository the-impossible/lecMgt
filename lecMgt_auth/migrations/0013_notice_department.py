# Generated by Django 4.2.1 on 2023-06-22 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("lecMgt_auth", "0012_alter_lecturerprofile_employment_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="notice",
            name="department",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="lecMgt_auth.department",
            ),
        ),
    ]