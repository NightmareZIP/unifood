# Generated by Django 4.2 on 2025-04-04 22:17

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("tarif", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Company",
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
                ("name", models.CharField(max_length=255, unique=True)),
                ("inn", models.CharField(max_length=255)),
                ("country", models.CharField(blank=True, max_length=255, null=True)),
                ("place", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "contact_person",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "contact_phone",
                    models.CharField(
                        blank=True,
                        max_length=12,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Телефон формата: '+999999999'.",
                                regex="^\\+?1?\\d{9,15}$",
                            )
                        ],
                    ),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "description",
                    models.TextField(blank=True, max_length=255, null=True),
                ),
                (
                    "tarif",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tarif.tarif",
                    ),
                ),
            ],
        ),
    ]
