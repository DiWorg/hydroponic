from rest_framework import permissions

from hydroponics.models import HydroponicSystem, Measurement, Sensor


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, HydroponicSystem):
            return obj.owner == request.user
        elif isinstance(obj, Sensor):
            return obj.system.owner == request.user
        elif isinstance(obj, Measurement):
            return obj.sensor.system.owner == request.user
        return False
