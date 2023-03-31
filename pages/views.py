from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
import csv
from django.http import HttpResponse
from django.contrib.auth.models import User, Group

# Create your views here.
def home(request):
    image = AppImage.objects.filter(name='home_image').first()
    if image:
        context = {'image': image}
    else:
        context = {'image': ''}
    return render(request, 'pages/home.html', context=context)

def feedback(request):
    if request.method == "POST":
        feedback = Feedback()
        feedback.registration_no = request.POST['reg_no']
        feedback.room = Room.objects.get(number=request.POST['room'])
        feedback.issue_type = request.POST['it']
        feedback.issue = request.POST['issue']
        feedback.save()
        return redirect('home')

    issue_types = (
        'Faculty Absent',
        'Web Application Issue',
        'WIFI issue',
        'Others',
    )
    instructions = ''
    feedback_content = ''
    rooms = Room.objects.all()
    context = {'issue_types': issue_types, 'rooms': rooms, 'instructions': instructions, 'feedback_content': feedback_content}
    return render(request, 'pages/feedback.html', context=context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username (or) Password is incorrect')

    context = {}
    return render(request, 'pages/login.html', context)

def logoutUser(request):
    if not request.user.is_authenticated:
        return redirect('home')
    messages.success(request, f'{request.user} has been succesfully logged out.')
    logout(request)
    return redirect('login')

def update_rooms(request):
    teams = Team.objects.all()
    reviews = Review.objects.all()
    for team in teams:
        for review in reviews:
            trr = TeamReviewRoom()
            trr.team = team
            trr.review = review
            trr.save()
    with open('rooms_ranges.csv') as file:
        csv_reader = csv.reader(file)
        c = 0
        for row in csv_reader:
            if c == 0:
                c += 1
            else:
                course = row[0]
                cluster = int(row[1])
                min_team = int(row[2])
                max_team = int(row[3])
                room_no = row[4]
                room = Room.objects.get(number=room_no)
                teams = Team.objects.filter(cluster=cluster, course=course, number__gte=min_team, number__lte=max_team)
                trrs = TeamReviewRoom.objects.filter(team__in=teams)
                trrs.update(room=room)
    return HttpResponse('done')

def faculty_upload(request):
    group = Group.objects.get(name='FACULTY')
    with open('faculty.csv') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            user = User()
            user.username = row[0]
            user.set_password(f'klu_{row[0]}')
            user.first_name = row[1]
            try:
                user.save()
                user.groups.add(group)
                user.save()
            except:
                print(user.username)
    return HttpResponse('done')