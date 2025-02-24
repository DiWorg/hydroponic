from django.db import models
from django.conf import settings

class HydroponicSystem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name="hydroponic_systems")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Sensor(models.Model):
    SENSOR_TYPE_CHOICES = [
        ('PH', 'pH'),
        ('TEMP', 'Temperatura'),
        ('TDS', 'TDS'),
    ]

    system = models.ForeignKey(HydroponicSystem, on_delete=models.CASCADE,
                               related_name="sensors")
    sensor_type = models.CharField(max_length=10, choices=SENSOR_TYPE_CHOICES,
                                   help_text="Wybierz typ czujnika")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.get_sensor_type_display()})"

class Measurement(models.Model):
    system = models.ForeignKey(HydroponicSystem, on_delete=models.CASCADE,
                               related_name="measurements")
    ph = models.DecimalField(max_digits=4, decimal_places=2)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    tds = models.IntegerField()
    measured_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.system.name} - {self.measured_at}"
