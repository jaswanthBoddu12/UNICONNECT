from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json

from .forms import AddStudentForm, EditStudentForm

from .models import CustomUser, Clubs, Notices, Students, Event, FeedBackStudent


def student_home(request):
    print(request.user.user_type)
    all_student_count = Students.objects.all().count()
    notice_count = Notices.objects.all().count()
    club_count = Clubs.objects.all().count()
    event_count = Event.objects.all().count()

    # For Clubs
    club_all = Clubs.objects.all()
    club_name_list = []
    for club in club_all:
        club_name_list.append(club.club_name)

    # For Notices
    notice_all = Notices.objects.all()
    notice_name_list = []
    for notice in notice_all:
        notice_name_list.append(notice.notice_name)
    
    # For Events
    event_all = Event.objects.all()
    event_name_list = []
    for event in event_all:
        event_name_list.append(event.event_name)
    
    context={
        "all_student_count": all_student_count,
        "notice_count": notice_count,
        "club_count": club_count,
        "event_count": event_count,
        "club_name_list": club_name_list,
        # "notice_count_list": notice_count_list,
        # "event_count_list": event_count_list,
        # "student_count_list_in_club": student_count_list_in_club,
        # "notice_list": notice_list,
        # "event_list": event_list,
        # "student_count_list_in_notice": student_count_list_in_notice,  
        #"student_name_list": student_name_list,
    }
    return render(request, "student_template/student_home_template.html")



def view_event(request):
    events = Event.objects.all()
    context = {
        "events": events
    }
    return render(request, "student_template/view_event_template.html", context)

def view_notice(request):
    notices = Notices.objects.all()
    context = {
        "notices": notices
    }
    return render(request, 'student_template/view_notice_template.html', context)

def view_club(request):
    clubs = Clubs.objects.all()
    context = {
        "clubs": clubs
    }
    return render(request, 'student_template/view_club_template.html', context)



def student_feedback(request):
    student_obj = Students.objects.get(admin=request.user.id)
    feedback_data = FeedBackStudent.objects.filter(student_id=student_obj)
    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'student_template/student_feedback.html', context)


def student_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('student_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        student_obj = Students.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackStudent(student_id=student_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('student_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('student_feedback')


def student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Students.objects.get(admin=user)

    context={
        "user": user,
        "student": student
    }
    return render(request, 'student_template/student_profile.html', context)


def student_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('student_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            student = Students.objects.get(admin=customuser.id)
            student.address = address
            student.save()
            
            messages.success(request, "Profile Updated Successfully")
            return redirect('student_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('student_profile')






