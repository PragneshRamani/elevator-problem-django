from django.contrib import admin
from elevators.models import Elevator, Floor, Request


class ElevatorAdmin(admin.ModelAdmin):
    pass


class FloorAdmin(admin.ModelAdmin):
    pass


class RequestAdmin(admin.ModelAdmin):
    pass

admin.site.register(Elevator, ElevatorAdmin)
admin.site.register(Floor, FloorAdmin)
admin.site.register(Request, RequestAdmin)


