from django.shortcuts import render, redirect
from pages.models import Review, Room, TeamReviewRoom, Student, Team, StudentReviewAttendance, StudentReviewScore, AppImage
from django.contrib import messages
from django.urls import reverse

# Create your views here.
def home(request):
    image = AppImage.objects.filter(name='learnathon_home_image').first()
    context = {'image': image}
    return render(request, 'learnathon/home.html', context)


def rooms(request):
    if not request.user.is_authenticated:
        return redirect('login')
    rooms = Room.objects.all().order_by('number')
    f0 = rooms.filter(floor='Ground Floor')
    f1 = rooms.filter(floor='First Floor')
    f2 = rooms.filter(floor='Second Floor')
    f3 = rooms.filter(floor='Third Floor')
    f4 = rooms.filter(floor='Fourth Floor')
    f5 = rooms.filter(floor='Fifth Floor')
    f6 = rooms.filter(floor='Sixth Floor')

    context = {'f0': f0, 'f1': f1, 'f2': f2, 'f3': f3, 'f4': f4, 'f5': f5, 'f6': f6}

    return render(request, 'learnathon/rooms.html', context=context)

def review_page(request, room_no):
    if not request.user.is_authenticated:
        return redirect('login')
    reviews = Review.objects.all()
    room = Room.objects.get(number=room_no)
    context = {'room': room, 'reviews': reviews}

    return render(request, 'learnathon/review_page.html', context=context)

def review_room_attendance(request, number, room_no):
    if not request.user.is_authenticated:
        return redirect('login')
    review = Review.objects.get(number=number)
    if not review.attendance_open:
        return redirect('learnathon_review_page', room_no=room_no)
    room = Room.objects.get(number=room_no)
    teams = TeamReviewRoom.get_teams_with_review_room(review, room)
    students = Student.objects.filter(team__in=teams).order_by('-team')
    if request.method == "POST":
        absentees = request.POST.getlist('absentees')
        StudentReviewAttendance.objects.filter(student__in=students, review=review).update(posted_by=request.user, absent=False)
        StudentReviewAttendance.objects.filter(review=review, student__registration_no__in=absentees).update(posted_by=request.user, absent=True)

        return redirect('learnathon_review_page', room_no=room_no)
    
    it = students.iterator()

    students_attendance = []
    for student in it:
        stu, created = StudentReviewAttendance.objects.get_or_create(student=student, review=review)
        students_attendance.append(stu)

    context = {'review_no': number, 'room_no': room_no, 'students_attendance': students_attendance}
    return render(request, 'learnathon/attendance.html', context=context)

def student_form(request):
    if request.method == "POST":
        reg_no = request.POST['reg_no']
        student = Student.objects.filter(registration_no=reg_no).first()
        attendances = StudentReviewAttendance.objects.filter(student=student).order_by('review__number')

        context = {'attendances': attendances, 'student': student}
        return render(request, 'learnathon/student_form.html', context=context)
    context = {}
    return render(request, 'learnathon/student_form.html', context=context)

def review_score_post(request, review_no, room_no):
    if not request.user.is_authenticated:
        return redirect('login')
    room = Room.objects.get(number=room_no)
    review = Review.objects.get(number=review_no)
    if not review.scoring_open:
        return redirect('learnathon_review_page', room_no=room_no)
    trrs = TeamReviewRoom.objects.filter(room=room, review=review).first()
    context = {'review_no': review_no, 'room_no': room_no}
    if trrs:
        context['teams'] = TeamReviewRoom.get_teams_with_review_room(review, room)
    else:
        context['teams'] = []
    
    return render(request, 'learnathon/review_post_score.html', context=context)

def review_score_post_form(request, review_no, team_no):
    if not request.user.is_authenticated:
        return redirect('login')
    review = Review.objects.get(number=review_no)
    team = Team.objects.get(name=team_no)
    students = Student.objects.filter(team=team).order_by('registration_no')
    room = TeamReviewRoom.objects.get(team=team, review=review).room
    if (not review.scoring_open) or (not review.score_required):
        return redirect('learnathon_review_page', room_no=room.number)

    v = StudentReviewScore.objects.filter(student=students.first(), review=review).first()
    if v and v.comments:
        context = {'prev_page_url': reverse('learnathon_review_page', args=[room.number]), 'room_no': room.number, 'message': 'Score has already been posted'}
        return render(request, 'learnathon/access_denied.html', context=context)
    
    if request.method == "POST":
        student_review_scores = StudentReviewScore.objects.filter(student__in=students, review=review)
        it = student_review_scores.iterator()
        for student_score in it:
            student_score.posted_by = request.user
            student_score.score = request.POST[f'score_{student_score.student.registration_no}']
            student_score.comments = request.POST[f'comments_{student_score.student.registration_no}']
            student_score.save()
        return redirect('learnathon_review_page', room_no=room.number)

    student_review_scores = []
    for student in students:
        student_review_scores.append(StudentReviewScore.objects.get_or_create(review=review, student=student)[0])
    context = {'student_review_scores': student_review_scores, 'instructions': review.instructions.split('\n'), 'questions': review.questions.split('\n'), 'team_no': team.name, 'course': team.course, 'review_no': review_no}
    return render(request, 'learnathon/review_post_score_form.html', context=context)

def report(request):
    if not request.user.is_superuser:
        return redirect('learnathon_home')
    context = {}
    return render(request, 'learnathon/report.html', context=context)