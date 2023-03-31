from django.urls import path
from .views import home, feedback, loginPage, logoutUser, update_rooms, faculty_upload

urlpatterns = [
    path('', home, name='home'),
    path('feedback/', feedback, name='feedback'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('room_allocation/', update_rooms, name='update-rooms'),
    path('faculty_upload', faculty_upload, name='faculty-upload'),
]
