# Generated by Django 4.2.1 on 2023-06-04 08:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("lecMgt_auth", "0003_leave"),
    ]

    operations = [
        migrations.CreateModel(
            name="Notice",
            fields=[
                (
                    "notice_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("notice_title", models.CharField(max_length=50, unique=True)),
                ("notice_detail", models.TextField(blank=True, null=True)),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date_created"
                    ),
                ),
                (
                    "posted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"verbose_name_plural": "Notice", "db_table": "Notice",},
        ),
    ]
