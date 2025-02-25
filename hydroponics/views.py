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

"""
Defintion of ViewSets for HydroponicSystem, Sensor, and Measurement.
Handling of CRUD operations, filtering, ordering, pagination, and permission checks.
"""


class HydroponicSystemViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing HydroponicSystem objects.

    Provides:
      - GET (list/retrieve): List or detail view of systems.
      - POST: Create a new system.
      - PUT/PATCH: Update an existing system.
      - DELETE: Delete a system.

    Features: filters, ordering, pagination, permissions.

    Attributes:
        queryset: Base queryset restricted to systems owned by the logged-in user.
        serializer_class: Default serializer.
        permission_classes: List of permission checks.
        pagination_class: Custom pagination class.
        filter_backends: List of filter backends.
        filterset_fields: Dict specifying how to filter.
        ordering_fields: List of fields allowed for ordering.
        ordering: Default ordering.
    """

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
        """
        Chooses between the basic serializer (list) and the detailed serializer (retrieve).
        """
        if self.action == "list":
            return HydroponicSystemSerializer
        if self.action == "retrieve":
            return HydroponicSystemDetailSerializer
        return HydroponicSystemSerializer

    def get_queryset(self):
        """
        Restricts the queryset to HydroponicSystems owned by the current user.
        """
        return HydroponicSystem.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """
        Sets the owner of the created HydroponicSystem to the current user.
        """
        serializer.save(owner=self.request.user)


class SensorViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing Sensor objects.

    Provides:
      - GET (list/retrieve): List or detail view of sensors.
      - POST: Create a new sensor.
      - PUT/PATCH: Update an existing sensor.
      - DELETE: Delete a sensor.

    Features: filtering, ordering, pagination, permissions.

    Attributes:
        queryset: Base queryset restricted to sensors belonging to systems owned by the user.
        serializer_class: Default serializer.
        permission_classes: List of permission checks.
        pagination_class: Custom pagination class.
        filter_backends: List of filter backends.
        filterset_class: The custom SensorFilter for advanced filtering.
        ordering_fields: Fields allowed for ordering.
        ordering: Default ordering.
    """

    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = AddPageNumberPagination

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = SensorFilter
    ordering_fields = ["name", "sensor_type", "system", "system__name"]
    ordering = ["name"]

    def get_queryset(self):
        """
        Restricts the queryset to sensors in systems owned by the current user.
        """
        return Sensor.objects.filter(system__owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save()


class MeasurementViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing Measurement objects.

    Provides:
      - GET (list/retrieve): List or detail view of measurements.
      - POST: Create a new measurement.
      - PUT/PATCH: Update an existing measurement.
      - DELETE: Delete a measurement.

    Features: filtering, ordering, pagination, permissions.

    Attributes:
        queryset: Base queryset restricted to measurements in systems owned by the user.
        serializer_class: Default serializer.
        permission_classes: List of permission checks.
        pagination_class: Custom pagination class.
        filter_backends: List of filter backends.
        filterset_class: The custom SensorFilter for advanced filtering.
        ordering_fields: Fields allowed for ordering.
        ordering: Default ordering.
    """

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
        """
        Restricts the queryset to measurements in systems owned by the current user.
        """
        return Measurement.objects.filter(sensor__system__owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save()
