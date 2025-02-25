from django.shortcuts import render
from rest_framework import viewsets
from .models import HydroponicSystem, Sensor, Measurement
from .permissions import IsOwner
from .serializers import HydroponicSystemSerializer, SensorSerializer, MeasurementSerializer
from rest_framework.permissions import IsAuthenticated


class HydroponicSystemViewSet(viewsets.ModelViewSet):
    queryset = HydroponicSystem.objects.all()
    serializer_class = HydroponicSystemSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return HydroponicSystem.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Sensor.objects.filter(system__owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

class MeasurementViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Measurement.objects.filter(sensor__system__owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save()