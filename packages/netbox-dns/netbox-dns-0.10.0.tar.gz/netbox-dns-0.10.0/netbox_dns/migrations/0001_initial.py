# Generated by Django 3.2.5 on 2021-08-13 14:44

import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("extras", "0059_exporttemplate_as_attachment"),
    ]

    operations = [
        migrations.CreateModel(
            name="NameServer",
            fields=[
                ("created", models.DateField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=django.core.serializers.json.DjangoJSONEncoder,
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255, unique=True)),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        through="extras.TaggedItem", to="extras.Tag"
                    ),
                ),
            ],
            options={
                "ordering": ("name", "id"),
            },
        ),
        migrations.CreateModel(
            name="Zone",
            fields=[
                ("created", models.DateField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=django.core.serializers.json.DjangoJSONEncoder,
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255, unique=True)),
                (
                    "status",
                    models.CharField(blank=True, default="active", max_length=50),
                ),
                (
                    "nameservers",
                    models.ManyToManyField(
                        blank=True, related_name="zones", to="netbox_dns.NameServer"
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        blank=True, through="extras.TaggedItem", to="extras.Tag"
                    ),
                ),
            ],
            options={
                "ordering": ("name", "id"),
            },
        ),
        migrations.CreateModel(
            name="Record",
            fields=[
                ("created", models.DateField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=django.core.serializers.json.DjangoJSONEncoder,
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("type", models.CharField(max_length=10)),
                ("name", models.CharField(max_length=255)),
                ("value", models.CharField(max_length=1000)),
                ("ttl", models.PositiveIntegerField()),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        through="extras.TaggedItem", to="extras.Tag"
                    ),
                ),
                (
                    "zone",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="netbox_dns.zone",
                    ),
                ),
            ],
            options={
                "ordering": ("name", "id"),
            },
        ),
    ]
