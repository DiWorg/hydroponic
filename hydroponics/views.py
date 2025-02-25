from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from .filters import MeasurementFilter, SensorFilter
from .models import HydroponicSystem, Measurement, Sensor
from .pagination import AddPageNumberPagination
from .permissions import IsOwner
from .serializers import (HydroponicSystemDetailSerializer,
                          HydroponicSystemSerializer, MeasurementSerializer,
                          SensorSerializer)


class HydroponicSystemViewSet(viewsets.ModelViewSet):
    queryset = HydroponicSystem.objects.all()
    serializer_class = HydroponicSystemSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = AddPageNumberPagination

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        "name": ["icontains"],
        "created_at": ["gte", "lte"],
    }

    ordering_fields = ["name", "created_at"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action == "list":
            return HydroponicSystemSerializer
        if self.action == "retrieve":
            return HydroponicSystemDetailSerializer
        return HydroponicSystemSerializer

    def get_queryset(self):
        return HydroponicSystem.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = AddPageNumberPagination

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = SensorFilter
    ordering_fields = ["name", "sensor_type", "system", "system__name"]
    ordering = ["name"]

    def get_queryset(self):
        return Sensor.objects.filter(system__owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save()


class MeasurementViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = AddPageNumberPagination

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MeasurementFilter
    ordering_fields = [
        "value",
        "measured_at",
        "sensor__name",
        "sensor__system",
        "sensor__system__name",
        "sensor__sensor_type",
    ]
    ordering = ["-measured_at"]

    def get_queryset(self):
        return Measurement.objects.filter(sensor__system__owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save()
