from django.shortcuts import render
from rest_framework import viewsets
from .models import HydroponicSystem, Sensor, Measurement
from .serializers import HydroponicSystemSerializer, SensorSerializer, MeasurementSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class HydroponicSystemViewSet(viewsets.ModelViewSet):
    queryset = HydroponicSystem.objects.all()
    serializer_class = HydroponicSystemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class MeasurementViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]