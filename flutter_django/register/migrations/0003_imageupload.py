# Generated by Django 4.2.4 on 2023-10-10 17:07

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("register", "0002_user_birth_user_farm_user_gender_user_number_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ImageUpload",
            fields=[
                (
                    "imageUrl",
                    models.CharField(
                        default="x",
                        max_length=1000,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "upload_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "is_done",
                    models.BooleanField(
                        default=False, verbose_name="Inspection complete"
                    ),
                ),
                (
                    "Edwardsiella",
                    models.DecimalField(
                        decimal_places=2, default=Decimal("0.00"), max_digits=2
                    ),
                ),
                (
                    "Vibrio",
                    models.DecimalField(
                        decimal_places=2, default=Decimal("0.00"), max_digits=2
                    ),
                ),
                (
                    "Streptococcus",
                    models.DecimalField(
                        decimal_places=2, default=Decimal("0.00"), max_digits=2
                    ),
                ),
                (
                    "Tenacibaculumn",
                    models.DecimalField(
                        decimal_places=2, default=Decimal("0.00"), max_digits=2
                    ),
                ),
                (
                    "Enteromyxum",
                    models.DecimalField(
                        decimal_places=2, default=Decimal("0.00"), max_digits=2
                    ),
                ),
                (
                    "Miamiensis",
                    models.DecimalField(
                        decimal_places=2, default=Decimal("0.00"), max_digits=2
                    ),
                ),
                (
                    "VHSV",
                    models.DecimalField(
                        decimal_places=2, default=Decimal("0.00"), max_digits=2
                    ),
                ),
                (
                    "upload_user",
                    models.ForeignKey(
                        db_column="id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="uploaded",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]