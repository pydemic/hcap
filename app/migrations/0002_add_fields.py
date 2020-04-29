# Generated by Django 3.0.5 on 2020-04-11 17:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("app", "0001_initial"),
        ("locations", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="notifierforhealthcareunit",
            name="notifier",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Notificador",
            ),
        ),
        migrations.AddField(
            model_name="notifierforhealthcareunit",
            name="unit",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="app.HealthcareUnit",
                verbose_name="Estabelecimento de Saúde",
            ),
        ),
        migrations.AddField(
            model_name="logentry",
            name="notifier",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="daily_notifications",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Usuário notificador",
            ),
        ),
        migrations.AddField(
            model_name="logentry",
            name="unit",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="notifications",
                to="app.HealthcareUnit",
                verbose_name="Estabelecimento de Saúde",
            ),
        ),
        migrations.AddField(
            model_name="healthcareunit",
            name="city",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="healthcare_units",
                to="locations.City",
                verbose_name="Município",
            ),
        ),
        migrations.AddField(
            model_name="capacity",
            name="notifier",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="capacity_notifications",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Usuário notificador",
            ),
        ),
        migrations.AddField(
            model_name="capacity",
            name="unit",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="capacity_notifications",
                to="app.HealthcareUnit",
                verbose_name="Unidade de saúde",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="notifierforhealthcareunit", unique_together={("notifier", "unit")}
        ),
    ]