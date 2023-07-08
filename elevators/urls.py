from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from elevators.views import ElevatorSystemViewSet, RequestViewSet, ElevatorViewSet

urlpatterns = [
    path('api/elevator-system/', ElevatorSystemViewSet.as_view({'post': 'create'}), name='elevator-system-create'),
    path('api/requests/', RequestViewSet.as_view({'get': 'list', 'post': 'create'}), name='request-create'),
    path('api/elevators/<int:pk>/move/', ElevatorViewSet.as_view({'put': 'update'}), name='elevator-move'),
    path('api/elevators/<int:pk>/', ElevatorViewSet.as_view({'get': 'retrieve'}), name='elevator-detail'),
    path('api/elevators/<int:pk>/next-destination/', ElevatorViewSet.as_view({'get': 'retrieve_next_destination'}), name='elevator-next-destination'),
    path('api/elevators/<int:pk>/moving-direction/', ElevatorViewSet.as_view({'get': 'retrieve'}), name='elevator-moving-direction'),
    path('api/elevators/<int:pk>/not-working/', ElevatorViewSet.as_view({'patch': 'partial_update'}), name='elevator-not-working'),
    path('api/elevators/<int:pk>/open-doors/', ElevatorViewSet.as_view({'post': 'open_doors'}), name='elevator-open-doors'),
    path('api/elevators/<int:pk>/close-doors/', ElevatorViewSet.as_view({'post': 'close_doors'}), name='elevator-close-doors'),
]