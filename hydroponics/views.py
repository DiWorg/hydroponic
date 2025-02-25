from rest_framework import viewsets

from .filters import MeasurementFilter, SensorFilter
from .models import HydroponicSystem, Sensor, Measurement
from .permissions import IsOwner
from .serializers import HydroponicSystemSerializer, SensorSerializer, MeasurementSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class HydroponicSystemViewSet(viewsets.ModelViewSet):
    queryset = HydroponicSystem.objects.all()
    serializer_class = HydroponicSystemSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'name': ['icontains'],
        'created_at': ['gte', 'lte'],
    }

    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return HydroponicSystem.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = SensorFilter
    ordering_fields = ['name', 'sensor_type', 'system', 'system__name']
    ordering = ['name']

    def get_queryset(self):
        return Sensor.objects.filter(system__owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

class MeasurementViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MeasurementFilter
    ordering_fields = [
        'value', 'measured_at',
        'sensor__name',
        'sensor__system',
        'sensor__system__name',
        'sensor__sensor_type',
    ]
    ordering = ['-measured_at']

    def get_queryset(self):
        return Measurement.objects.filter(sensor__system__owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save()