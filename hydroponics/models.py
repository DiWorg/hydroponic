from django.conf import settings
from django.db import models

"""
Definitions of the following models:HydroponicSystem, 
Sensor, and Measurement.
"""


class HydroponicSystem(models.Model):
    """
    Represents a hydroponic system.

    Attributes:
        name: The system's name.
        description: Optional description of the system.
        owner: The user who owns this system.
        created_at: The date and time when the system was created.
    """

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="hydroponic_systems",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a representation combining the ID and the name.
        """
        return f"{self.id} – {self.name}"


class Sensor(models.Model):
    """
    Represents a sensor.

    Attributes:
       system: The system to which the sensor belongs.
       sensor_type: The sensor type (PH, TEMP, or TDS).
       name: The name or label of the sensor.
    """

    SENSOR_TYPE_CHOICES = [
        ("PH", "pH"),
        ("TEMP", "Temperature"),
        ("TDS", "TDS"),
    ]

    system = models.ForeignKey(
        HydroponicSystem, on_delete=models.CASCADE, related_name="sensors"
    )
    sensor_type = models.CharField(
        max_length=10, choices=SENSOR_TYPE_CHOICES, help_text="Choose sensor type."
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        """
        Returns a representation combining the ID, the name and sensor type.
        """
        return f"{self.id} – {self.name} ({self.get_sensor_type_display()})"


class Measurement(models.Model):
    """
    Represents a single measurement.

    Attributes:
        sensor: The sensor from which this measurement was taken.
        value: The measured value (e.g., pH, TDS, temperature).
        measured_at: The date and time the measurement was recorded.
    """

    sensor = models.ForeignKey(
        Sensor, on_delete=models.CASCADE, related_name="measurements"
    )
    value = models.DecimalField(max_digits=10, decimal_places=2)
    measured_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a representation combining the ID, the name and
        time of measurement.
        """
        return f"{self.id} - {self.sensor.name} - {self.measured_at}"
