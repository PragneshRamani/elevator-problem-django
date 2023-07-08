### Create virtualenv
- virtualenv venv

### Activate virtualenv
- source venv/bin/activate

### Install dependency
- pip install -r requirements.txt

### Run migrations
- python manage.py migrate

### Create super user
- python manage.py createsuperuser

### Run server
- python manage.py runserver

### DB Already pushed for testing purpose
- username - testuser
- password - test@123

## Video Link
- https://www.loom.com/share/6bd40639b7394549b45eb2da9f0cd238?sid=9cfc5d39-d48f-4d1a-b3d4-8cbb99595ab4

## APIs Details and DB you can use

- `POST /api/elevator-system/` - Create number of elevators in this elevator system
- `POST /api/requests/` - Create Request to move elevator up or down or stop
- `GET /api/requests/?elevator_id=` - Fetch All the requests of elevator
- `PATCH /api/elevators/<int:pk>/move/` - Move the Elevator up or down with optimal destination
- `GET /api/elevators/<int:pk>/next-destination/` - Fetch next destination floor based on request
- `GET /api/elevators/<int:pk>/moving-direction/` - Fetch moving direction of elevator
- `PATCH /api/elevators/<int:pk>/not-working/` - Mark elevator as in maintenance or not
- `POST /api/elevators/<int:pk>/open-doors/` - Open the elevator door
- `POST /api/elevators/<int:pk>/close-doors/` - Close the elevator door

#### Here we assume that Floor is already created in DB and All elevators are at first floor at a time of destination in case of any error you can set floor to 1 initially in elevator model.
