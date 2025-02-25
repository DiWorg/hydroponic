from rest_framework import serializers

from .models import HydroponicSystem, Measurement, Sensor

"""
Definition of serializers for the HydroponicSystem, Sensor, and Measurement models.
It includes validation logic for ownership and sensor measurement ranges.
"""

# Defines allowed ranges for different sensor types (e.g., pH, Temperature, TDS).
ALLOWED_RANGES = {
    "PH": (0, 14),
    "TEMP": (-50, 150),
    "TDS": (0, 9999),
}


class MeasurementSerializer(serializers.ModelSerializer):
    """
    Serializer for the Measurement model which validates:
      - The measurement value is within an allowed range for the sensor type.
      - The user is the owner of the system to which the sensor belongs.

    Attributes:
        Meta: Holds model and field definitions.
        __init__: Restricts sensor to those owned by the user.
        validate: Ensures the measurement value is within the allowed range.
        create: Checks system ownership before creating the measurement.
    """

    class Meta:
        model = Measurement
        fields = ["id", "sensor", "value", "measured_at"]
        read_only_fields = ["id", "measured_at"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            self.fields["sensor"].queryset = Sensor.objects.filter(system__owner=user)

    def validate(self, attrs):
        """
        Global validation method.
        Checks if 'value' is within the ALLOWED_RANGES.
        """

        sensor = attrs.get("sensor")
        value = attrs.get("value")

        if sensor and value is not None:
            sensor_type = sensor.sensor_type
            if sensor_type in ALLOWED_RANGES:
                min_val, max_val = ALLOWED_RANGES[sensor_type]
                if not (min_val <= value <= max_val):
                    raise serializers.ValidationError(
                        f"Value {value} is out of the scope {min_val}–{max_val} "
                        f"for sensor type: {sensor_type}."
                    )

        return attrs

    def create(self, validated_data):
        """
        Ensures that the user is the owner of the system before creating a measurement.
        """
        sensor = validated_data["sensor"]
        user = self.context["request"].user

        if sensor.system.owner != user:
            raise serializers.ValidationError("You cannot add another user's sensor.")

        return super().create(validated_data)


class SensorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Sensor model which validates:
      - The sensor belongs to a system owned by the logged-in user.

    Attributes:
        sensor_type_display: Displays the readable sensor type.
        measurements: Read-only nested measurements.
    """

    sensor_type_display = serializers.CharField(
        source="get_sensor_type_display", read_only=True
    )
    measurements = MeasurementSerializer(many=True, read_only=True)

    class Meta:
        model = Sensor
        fields = [
            "id",
            "system",
            "name",
            "sensor_type",
            "sensor_type_display",
            "measurements",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            self.fields["system"].queryset = HydroponicSystem.objects.filter(owner=user)

    def validate(self, attrs):
        """
        Checks if the system belongs to the current user.
        """
        system = attrs.get("system")
        user = self.context["request"].user
        if system.owner != user:
            raise serializers.ValidationError(
                "This system doesn't belong to this user."
            )
        return attrs


class HydroponicSystemSerializer(serializers.ModelSerializer):
    """
    Serializer for the HydroponicSystem model.

    Attributes:
        sensors: Read-only list of sensor IDs.
        owner: Shows the username of the owner.
        validate_name: Ensures non-dup system names for user.
    """

    sensors = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = HydroponicSystem
        fields = ["id", "name", "description", "owner", "sensors", "created_at"]

    def validate_name(self, value):
        user = self.context["request"].user
        system_id = self.instance.id if self.instance else None

        if HydroponicSystem.objects.filter(owner=user, name=value).exclude(id=system_id).exists():
            raise serializers.ValidationError(
                "You already have a system with that name."
            )
        return value


class HydroponicSystemDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed view of a HydroponicSystem,
    including 10 recent measurements.

    Attributes:
        sensors: Read-only list of sensor IDs.
        owner: Shows the username of the owner.
        last_10_measurements: Returns the 10 latest measurements
            for all sensors in the system.
    """

    sensors = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    owner = serializers.StringRelatedField(read_only=True)
    last_10_measurements = serializers.SerializerMethodField()

    class Meta:
        model = HydroponicSystem
        fields = [
            "id",
            "name",
            "description",
            "owner",
            "sensors",
            "created_at",
            "last_10_measurements",
        ]

    def get_last_10_measurements(self, obj):
        """
        Retrieves the 10 most recent measurements for all sensors in this system.
        """
        measurements = Measurement.objects.filter(sensor__system=obj).order_by(
            "-measured_at"
        )[:10]
        return MeasurementSerializer(measurements, many=True).data

    def validate_name(self, value):
        """
        Ensures non-dup system names for user.
        """
        user = self.context["request"].user
        system_id = self.instance.id if self.instance else None

        if HydroponicSystem.objects.filter(owner=user, name=value).exclude(id=system_id).exists():
            raise serializers.ValidationError(
                "You already have a system with that name."
            )
        return value
