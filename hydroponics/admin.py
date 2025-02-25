from django.contrib import admin

from .models import HydroponicSystem, Measurement, Sensor


@admin.register(HydroponicSystem)
class HydroponicSystemAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "created_at")
    search_fields = ("name", "owner__username")


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ("name", "sensor_type", "system")
    list_filter = ("sensor_type",)
    search_fields = ("name", "system__name")


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ("id", "sensor", "value", "measured_at")
    list_filter = ("sensor__sensor_type",)
    search_fields = ("sensor__name",)
