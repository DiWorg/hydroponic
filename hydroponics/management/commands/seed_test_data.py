from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from hydroponics.models import HydroponicSystem, Sensor, Measurement

class Command(BaseCommand):
    help = "Seeds the database with test data."

    def handle(self, *args, **options):
        user1, _ = User.objects.get_or_create(username='user1')
        user1.set_password('pass1')
        user1.save()

        user2, _ = User.objects.get_or_create(username='user2')
        user2.set_password('pass2')
        user2.save()

        def create_sensors_with_measurements(system):
            sensor_types = [
                ("PH", "pH Sensor"),
                ("TEMP", "Temp Sensor"),
                ("TDS", "TDS Sensor")
            ]
            for sensor_type, sensor_name in sensor_types:
                sensor, _ = Sensor.objects.get_or_create(
                    system=system,
                    sensor_type=sensor_type,
                    name=sensor_name
                )
                Measurement.objects.get_or_create(
                    sensor=sensor,
                    value=7.0 if sensor_type == "PH" else 20.0
                )

        for i in range(1, 3):
            system_user1, _ = HydroponicSystem.objects.get_or_create(
                owner=user1,
                name=f"User1 System{i}"
            )
            create_sensors_with_measurements(system_user1)

            system_user2, _ = HydroponicSystem.objects.get_or_create(
                owner=user2,
                name=f"User2 System{i}"
            )
            create_sensors_with_measurements(system_user2)

        self.stdout.write(self.style.SUCCESS("Test data seeded successfully!"))