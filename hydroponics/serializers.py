from rest_framework import serializers
from .models import HydroponicSystem, Sensor, Measurement

class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['id', 'sensor', 'value', 'measured_at']
        read_only_fields = ['id', 'measured_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            self.fields['sensor'].queryset = Sensor.objects.filter(system__owner=user)

    def create(self, validated_data):
        sensor = validated_data['sensor']
        user = self.context['request'].user

        if sensor.system.owner != user:
            raise serializers.ValidationError("Nie możesz dodać pomiaru do cudzego systemu.")

        return super().create(validated_data)

class SensorSerializer(serializers.ModelSerializer):
    sensor_type_display = serializers.CharField(source='get_sensor_type_display',
                                                read_only=True)
    measurements = MeasurementSerializer(many=True, read_only=True)

    class Meta:
        model = Sensor
        fields = ['id', 'system', 'name', 'sensor_type', 'sensor_type_display',
                  'measurements']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            self.fields['system'].queryset = HydroponicSystem.objects.filter(owner=user)

    def validate(self, attrs):
        system = attrs.get('system')
        user = self.context['request'].user
        if system.owner != user:
            raise serializers.ValidationError("System nie należy do zalogowanego użytkownika.")
        return attrs

class HydroponicSystemSerializer(serializers.ModelSerializer):
    sensors = SensorSerializer(many=True, read_only=True)
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = HydroponicSystem
        fields = ['id', 'name', 'description', 'owner', 'sensors', 'created_at']

    def validate_name(self, value):
        user = self.context['request'].user
        if HydroponicSystem.objects.filter(owner=user, name=value).exists():
            raise serializers.ValidationError("Masz już system o tej nazwie.")
        return value