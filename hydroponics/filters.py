import django_filters

from .models import HydroponicSystem, Measurement, Sensor

"""
Definition of custom filters (based on django-filter) for 
searching and filtering data.
"""


class MeasurementFilter(django_filters.FilterSet):
    """
    A filter that allows searching measurements by various types
    of data.

    In Meta fields:
        sensor__system: Filter measurements by system ID.
        sensor__system__name: Filter by system name.
        sensor__sensor_type: Filter by sensor type (PH, TEMP, TDS).
        value: Filter by measurement value range.
        measured_at: Filter by measurement date range.

    Attributes:
        sensor__system: Initialization for list of systems
            connected to user.
        sensor: Initialization for list of sensors
            connected to user.
    """

    sensor__system = django_filters.ModelChoiceFilter(
        queryset=HydroponicSystem.objects.none(), label="System"
    )
    sensor = django_filters.ModelChoiceFilter(
        queryset=Sensor.objects.none(), label="Sensor"
    )

    class Meta:
        model = Measurement
        fields = {
            "sensor": ["exact"],
            "sensor__system": ["exact"],
            "sensor__system__name": ["icontains", "exact"],
            "sensor__sensor_type": ["exact"],
            "value": ["gte", "lte"],
            "measured_at": ["gte", "lte"],
        }

    def __init__(self, *args, **kwargs):
        """
        Restricting list of systems and sensors
        to those owned by the logged-in user.
        """
        request = kwargs.get("request")
        super().__init__(*args, **kwargs)

        if request and hasattr(request, "user"):
            user = request.user
            self.filters["sensor__system"].queryset = HydroponicSystem.objects.filter(
                owner=user
            )
            self.filters["sensor"].queryset = Sensor.objects.filter(system__owner=user)


class SensorFilter(django_filters.FilterSet):
    """
    A filter that allows searching sensors by various types
    of data.

    In Meta fields:
        system: Filter by system ID.
        system__name: Filter by system name.
        sensor_type: Filter by sensor type (PH, TEMP, TDS).
        name: Filter by partial sensor name.

    Attributes:
        system: Initialization for list of systems
            connected to user.
    """

    system = django_filters.ModelChoiceFilter(
        queryset=HydroponicSystem.objects.none(), label="System"
    )

    class Meta:
        model = Sensor
        fields = {
            "system": ["exact"],
            "system__name": ["icontains", "exact"],
            "sensor_type": ["exact"],
            "name": ["icontains"],
        }

    def __init__(self, *args, **kwargs):
        """
        Restricting list of systems and sensors
        to those owned by the logged-in user.
        """
        super().__init__(*args, **kwargs)
        request = kwargs.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            self.filters["system"].queryset = HydroponicSystem.objects.filter(
                owner=user
            )
