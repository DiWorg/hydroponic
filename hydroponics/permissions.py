from rest_framework import permissions

from hydroponics.models import HydroponicSystem, Measurement, Sensor

"""
Definition of custom permission classes for the Hydroponic API,
verifying object ownership.
"""


class IsOwner(permissions.BasePermission):
    """
    A permission class ensuring that only the owner of a resource
    can access or modify it.

    - For HydroponicSystem, checks if obj.owner == request.user
    - For Sensor, checks if obj.system.owner == request.user
    - For Measurement, checks if obj.sensor.system.owner == request.user
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, HydroponicSystem):
            return obj.owner == request.user
        elif isinstance(obj, Sensor):
            return obj.system.owner == request.user
        elif isinstance(obj, Measurement):
            return obj.sensor.system.owner == request.user
        return False
