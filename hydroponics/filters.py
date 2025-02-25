import django_filters
from .models import Measurement, Sensor, HydroponicSystem

class MeasurementFilter(django_filters.FilterSet):
    sensor__system = django_filters.ModelChoiceFilter(
        queryset=HydroponicSystem.objects.none(),
        label="System"
    )
    sensor = django_filters.ModelChoiceFilter(
        queryset=Sensor.objects.none(),
        label="Sensor"
    )

    class Meta:
        model = Measurement
        fields = {
            'sensor': ['exact'],
            'sensor__system': ['exact'],
            'sensor__system__name': ['icontains', 'exact'],
            'sensor__sensor_type': ['exact'],
            'value': ['gte', 'lte'],
            'measured_at': ['gte', 'lte'],
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.get('request')
        super().__init__(*args, **kwargs)

        if request and hasattr(request, 'user'):
            user = request.user
            self.filters['sensor__system'].queryset = HydroponicSystem.objects.filter(owner=user)
            self.filters['sensor'].queryset = Sensor.objects.filter(system__owner=user)


class SensorFilter(django_filters.FilterSet):
    system = django_filters.ModelChoiceFilter(
        queryset=HydroponicSystem.objects.none(),
        label="System"
    )

    class Meta:
        model = Sensor
        fields = {
            'system': ['exact'],
            'system__name': ['icontains', 'exact'],
            'sensor_type': ['exact'],
            'name': ['icontains'],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = kwargs.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            self.filters['system'].queryset = HydroponicSystem.objects.filter(owner=user)