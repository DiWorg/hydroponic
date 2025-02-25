from django.conf import settings
from django.db import models


class HydroponicSystem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="hydroponic_systems",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} – {self.name}"


class Sensor(models.Model):
    SENSOR_TYPE_CHOICES = [
        ("PH", "pH"),
        ("TEMP", "Temperatura"),
        ("TDS", "TDS"),
    ]

    system = models.ForeignKey(
        HydroponicSystem, on_delete=models.CASCADE, related_name="sensors"
    )
    sensor_type = models.CharField(
        max_length=10, choices=SENSOR_TYPE_CHOICES, help_text="Wybierz typ czujnika"
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id} – {self.name} ({self.get_sensor_type_display()})"


class Measurement(models.Model):
    sensor = models.ForeignKey(
        Sensor, on_delete=models.CASCADE, related_name="measurements"
    )
    value = models.DecimalField(max_digits=10, decimal_places=2)
    measured_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.sensor.name} - {self.measured_at}"
