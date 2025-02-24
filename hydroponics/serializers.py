from rest_framework import serializers
from .models import HydroponicSystem, Sensor, Measurement

class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['id', 'sensor', 'value', 'measured_at']
        read_only_fields = ['id', 'measured_at']

class SensorSerializer(serializers.ModelSerializer):
    sensor_type_display = serializers.CharField(source='get_sensor_type_display',
                                                read_only=True)
    measurements = MeasurementSerializer(many=True, read_only=True)

    class Meta:
        model = Sensor
        fields = ['id', 'system', 'name', 'sensor_type', 'sensor_type_display',
                  'measurements']

class HydroponicSystemSerializer(serializers.ModelSerializer):
    sensors = SensorSerializer(many=True, read_only=True)
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = HydroponicSystem
        fields = ['id', 'name', 'description', 'owner', 'sensors', 'created_at']