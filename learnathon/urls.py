from django.urls import path
from .views import home, rooms, review_page, review_room_attendance, student_form, review_score_post, review_score_post_form

urlpatterns = [
    path('', home, name='learnathon_home'),
    path('rooms/', rooms, name='learnathon_rooms'),
    path('rooms/<str:room_no>', review_page, name='learnathon_review_page'),
    path('rooms/attendance/<int:number>/<str:room_no>', review_room_attendance, name='learnathon_review_room_attendance'),
    path('rooms/review/<int:review_no>/<str:room_no>', review_score_post, name='learnathon_review_score_post'),
    path('rooms/review/form/<int:review_no>/<str:team_no>', review_score_post_form, name='learnathon_review_score_post_form'),
    path('student_form/', student_form, name='student_form')
]
