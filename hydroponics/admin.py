from django.contrib import admin

from .models import HydroponicSystem, Measurement, Sensor

"""
Configuration of the Django Admin interface for the
HydroponicSystem, Measurement, and Sensor models.
"""


@admin.register(HydroponicSystem)
class HydroponicSystemAdmin(admin.ModelAdmin):
    """
    Admin configuration for the HydroponicSystem model.

    Attributes:
        list_display: Fields on the admin list page.
        search_fields:: Fields used for search in the admin page.
    """

    list_display = ("name", "owner", "created_at")
    search_fields = ("name", "owner__username")


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Sensor model.

    Attributes:
       list_display: Fields on the admin list page.
       list_filter: Fields used for filtering in the admin page.
       search_fields: Fields used for search in the admin page.
    """

    list_display = ("name", "sensor_type", "system")
    list_filter = ("sensor_type",)
    search_fields = ("name", "system__name")


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Measurement model.

    Attributes:
        list_display: Fields on the admin list page.
        list_filter: Fields used for filtering in the admin page.
        search_fields: Fields used for search in the admin page.
    """

    list_display = ("id", "sensor", "value", "measured_at")
    list_filter = ("sensor__sensor_type",)
    search_fields = ("sensor__name",)
