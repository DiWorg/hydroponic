from django.contrib import admin
from .models import HydroponicSystem, Measurement, Sensor

admin.site.register(HydroponicSystem)
admin.site.register(Sensor)
admin.site.register(Measurement)