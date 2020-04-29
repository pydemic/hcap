# Generated by Django 3.0.5 on 2020-04-21 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SeedState",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("app", models.CharField(max_length=30, verbose_name="app name")),
                ("model", models.CharField(max_length=30, verbose_name="model name")),
                (
                    "context",
                    models.CharField(
                        blank=True, default="default", max_length=30, verbose_name="seed context"
                    ),
                ),
                (
                    "kind",
                    models.CharField(
                        blank=True, default="base", max_length=30, verbose_name="seed type"
                    ),
                ),
                ("seeded", models.BooleanField(blank=True, default=False, verbose_name="seeded")),
                ("seeded_at", models.DateTimeField(auto_now=True, verbose_name="date of seeding")),
            ],
            options={
                "verbose_name": "seed state",
                "verbose_name_plural": "seed states",
                "unique_together": {("app", "model", "kind")},
            },
        ),
    ]
