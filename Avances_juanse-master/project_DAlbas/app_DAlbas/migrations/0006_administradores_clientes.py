# Generated by Django 4.2.2 on 2023-08-01 23:39

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app_DAlbas", "0005_delete_administradores_delete_clientes"),
    ]

    operations = [
        migrations.CreateModel(
            name="Administradores",
            fields=[
                (
                    "user_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "cargoAdministrador",
                    models.CharField(
                        db_comment="Cargo que ocupa el administrador a registrar",
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "fechaHoraCreacionAdmin",
                    models.DateTimeField(
                        auto_now_add=True, db_comment="Fecha y hora del registro"
                    ),
                ),
                (
                    "fechaHoraActualizacionAdmin",
                    models.DateTimeField(
                        auto_now=True, db_comment="Fecha y hora última actualización"
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            bases=("app_DAlbas.user",),
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Clientes",
            fields=[
                (
                    "user_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "identificacionCliente",
                    models.CharField(
                        db_comment="Identificación del cliente, puede ser cédula o NUIP",
                        max_length=20,
                        unique=True,
                    ),
                ),
                (
                    "direccionCliente",
                    models.CharField(
                        db_comment="Dirección de residencia del cliente",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "telefonoCliente",
                    models.CharField(
                        db_comment="Número telefono del cliente",
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "fechaHoraCreacionCliente",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_comment="Fecha y hora del registro del cliente",
                    ),
                ),
                (
                    "fechaHoraActualizacionCliente",
                    models.DateTimeField(
                        auto_now=True, db_comment="Fecha y hora última actualización"
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            bases=("app_DAlbas.user",),
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
