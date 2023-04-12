from django.urls import path
from .views import home, feedback, loginPage, logoutUser, update_rooms, faculty_upload, attendance_status, reports_page, update_it_attendance

urlpatterns = [
    path('', home, name='home'),
    path('feedback/', feedback, name='feedback'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('room_allocation/', update_rooms, name='update-rooms'),
    path('faculty_upload', faculty_upload, name='faculty-upload'),
    path('attendance_status/', attendance_status, name='attendance-status'),
    path('reports_page', reports_page, name='report-form'),
    path('att_upt', update_it_attendance, name='t-att'),
]

