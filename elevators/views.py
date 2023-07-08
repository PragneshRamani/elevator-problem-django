from rest_framework import viewsets, status
from rest_framework.response import Response
from elevators.models import Elevator, Floor, Request
from elevators.serializers import ElevatorSerializer, FloorSerializer, RequestSerializer


# Initialize the elevator system to create 'n' elevators in the system
class ElevatorSystemViewSet(viewsets.ViewSet):
    """
        You need to pass below request params to create elevator system
        {
            "num_elevators": 2
        }
    """
    def create(self, request):
        num_elevators = request.data.get('num_elevators')
        for _ in range(num_elevators):
            Elevator.objects.create()
        return Response({'message': f'Elevator system initialized with {num_elevators} elevators.'}, status=status.HTTP_201_CREATED)


class ElevatorViewSet(viewsets.ModelViewSet):
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer

    def move_elevator(self, elevator):
        requests = Request.objects.filter(elevator=elevator).order_by('floor__floor_number')
        # Check if Request exist for given elevator
        if requests.exists():
            destination_floor = requests.first().floor.floor_number
            elevator_current_floor = elevator.current_floor.floor_number

            count = elevator_current_floor

            # Go till reach to the destination floor
            while count != destination_floor:
                if count < destination_floor:
                    elevator.direction = 'up'
                    elevator.current_floor = Floor.objects.filter(floor_number__gt=count).order_by('floor_number').first()
                    count += 1 
                else:
                    elevator.direction = 'down'
                    elevator.current_floor = Floor.objects.filter(floor_number__lt=count).order_by('-floor_number').first()
                    count -= 1
                elevator.save()
                print(f'Elevator {elevator.id} is moving {elevator.direction}. reached at {count}')
            print('Elevator has arrived at the destination floor.')
            requests.first().delete()
            elevator.direction = ''
            elevator.save()
            return Response({'message': 'Elevator has arrived at the destination floor.'}, status=status.HTTP_200_OK)

        else:
            elevator.direction = ''
            elevator.save()
            return Response({'message': f'Elevator {elevator.id} is currently not in service.'}, status=status.HTTP_200_OK)

    # Fetch if the elevator is moving up or down currently
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.direction == '':
            return Response({'message': 'Elevator is currently not in service.'}, status=status.HTTP_200_OK)
        else:
            return Response({'direction': instance.direction}, status=status.HTTP_200_OK)

    # Fetch the next destination floor for a given elevator
    def retrieve_next_destination(self, request, *args, **kwargs):
        instance = self.get_object()
        next_floor = Request.objects.filter(elevator=instance).order_by('floor__floor_number').first()
        if next_floor is None:
            return Response({'message': 'No pending requests for this elevator.'}, status=status.HTTP_200_OK)
        else:
            serializer = FloorSerializer(next_floor.floor)
            return Response(serializer.data, status=status.HTTP_200_OK)

    # Move elevator based on Requests
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        elevator = self.perform_action(instance, serializer.validated_data)
        if elevator.direction == 'stop':
            elevator.save()
            return Response({'message': 'elevator stopped.'}, status=status.HTTP_200_OK)
        if elevator is None:
            return Response({'message': 'Invalid elevator action.'}, status=status.HTTP_400_BAD_REQUEST)
        return self.move_elevator(elevator)
    
    # Handle If Elevator is in Maintenance or not
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        is_operational = request.data.get('is_operational')
        is_maintenance = request.data.get('is_maintenance')

        if is_operational is not None:
            instance.is_operational = is_operational
        if is_maintenance is not None:
            instance.is_maintenance = is_maintenance

        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Open/close the door
    def perform_door_action(self, request, action):
        instance = self.get_object()
        if instance.is_operational and not instance.is_maintenance:
            if action == 'open':
                return Response({'message': f'Elevator {instance.id} doors are now open.'}, status=status.HTTP_200_OK)
            elif action == 'close':
                return Response({'message': f'Elevator {instance.id} doors are now closed.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Elevator is not in service or under maintenance.'}, status=status.HTTP_400_BAD_REQUEST)

    def open_doors(self, request, *args, **kwargs):
        return self.perform_door_action(request, 'open')

    def close_doors(self, request, *args, **kwargs):
        return self.perform_door_action(request, 'close')

    # Perform elevator direction or set to stop
    def perform_action(self, elevator, data):
        action = data.get('direction')
        if action == 'up' or action == 'down':
            elevator.direction = action
            return elevator
        elif action == 'stop':
            elevator.direction = ''
            return elevator
        return None


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    # Fetch all requests for a given elevator
    def list(self, request, *args, **kwargs):
        elevator_id = request.query_params.get('elevator_id')
        if elevator_id is None:
            return Response({'error': 'elevator_id parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        requests = Request.objects.filter(elevator__id=int(elevator_id))
        serializer = self.get_serializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Save a user request to the list of requests for an elevator
    def create(self, request, *args, **kwargs):
        floor_number = request.data.get('floor')
        if floor_number is None:
            return Response({'error': 'floor_number parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        floor = Floor.objects.filter(floor_number=floor_number).first()
        if floor is None:
            return Response({'error': 'Invalid floor_number.'}, status=status.HTTP_400_BAD_REQUEST)
        elevator = self.assign_elevator(floor)
        if elevator is None:
            return Response({'message': 'No available elevators at the moment.'}, status=status.HTTP_200_OK)
        request_obj = Request.objects.create(elevator=elevator, floor=floor)
        serializer = self.get_serializer(request_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Assign Elevator which is available and not in maintenance
    def assign_elevator(self, floor):
        elevators = Elevator.objects.filter(is_operational=True, is_maintenance=False, direction='')
        if elevators.exists():
            return elevators.order_by('id').first()
        return None
