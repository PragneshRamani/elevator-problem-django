from django.db import models

class Elevator(models.Model):
    is_operational = models.BooleanField(default=True)
    is_maintenance = models.BooleanField(default=False)
    current_floor = models.ForeignKey('Floor', on_delete=models.SET_NULL, null=True, blank=True)
    direction = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f'Elevator {self.id}'


class Floor(models.Model):
    floor_number = models.IntegerField(unique=True)

    def __str__(self):
        return f'Floor {self.floor_number}'


class Request(models.Model):
    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)

    def __str__(self):
        return f'Request: Elevator {self.elevator.id} to Floor {self.floor.floor_number}'