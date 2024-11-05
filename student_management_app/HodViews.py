from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json

from .forms import AddStudentForm, EditStudentForm

from .models import CustomUser, Clubs, Notices, Students, Event, FeedBackStudent


def admin_home(request):
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
    
    # For Students
    student_name_list=[]
    students = Students.objects.all()
    for student in students:
        student_name_list.append(student.admin.first_name)


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
        "student_name_list": student_name_list,
    }
    return render(request, "hod_template/home_content.html", context)



def add_club(request):
    return render(request, "hod_template/add_club_template.html")


def add_club_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_club')
    else:
        club_name = request.POST.get('club_name')
        club_lead = request.POST.get('club_lead')  # Updated field name
        club_lead_contact = request.POST.get('club_lead_contact')  # Updated field name
        club_desc = request.POST.get('description')
        # club_file = request.FILES.get('club_file', None)

        if not club_name or not club_lead or not club_lead_contact:
            messages.error(request, "Club Name, Lead, and Contact are required fields.")
            return redirect('add_club')

        try:
            club_model = Clubs(club_name=club_name, club_lead=club_lead, club_lead_contact=club_lead_contact, club_desc=club_desc)
            club_model.save()
            messages.success(request, "Club Added Successfully!")
            return redirect('add_club')
        except Exception as e:
            messages.error(request, f"Failed to Add Club: {str(e)}")
            return redirect('add_club')




def manage_club(request):
    clubs = Clubs.objects.all()
    context = {
        "clubs": clubs
    }
    return render(request, 'hod_template/manage_club_template.html', context)


def edit_club(request, club_id):
    club = Clubs.objects.get(id=club_id)
    context = {
        "club": club,
        "id": club_id
    }
    return render(request, 'hod_template/edit_club_template.html', context)

def edit_club_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method")
    else:
        club_id = request.POST.get('club_id')
        club_name = request.POST.get('club')
        club_lead = request.POST.get('club_lead')
        club_lead_contact = request.POST.get('club_lead_contact')
        club_desc = request.POST.get('club_desc')
        # club_file = request.POST.get('club_file')

        try:
            club = Clubs.objects.get(id=club_id)
            club.club_name = club_name
            club.club_lead = club_lead
            club.club_lead_contact = club_lead_contact
            club.club_desc = club_desc
            # club.club_file=club_file
            club.save()

            messages.success(request, "Club Updated Successfully.")
            return redirect('/edit_club/' + club_id)

        except:
            messages.error(request, "Failed to Update Club.")
            return redirect('/edit_club/' + club_id)



def delete_club(request, club_id):
    club = Clubs.objects.get(id=club_id)
    try:
        club.delete()
        messages.success(request, "club Deleted Successfully.")
        return redirect('manage_club')
    except:
        messages.error(request, "Failed to Delete club.")
        return redirect('manage_club')


def manage_event(request):
    events = Event.objects.all()
    context = {
        "events": events
    }
    return render(request, "hod_template/manage_event_template.html", context)


def add_event(request):
    return render(request, "hod_template/add_event_template.html")


def add_event_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_event')
    else:
        event_name = request.POST.get('event_name')
        event_organiser = request.POST.get('event_organiser')
        event_held_on = request.POST.get('event_held_on')
        event_desc = request.POST.get('event_desc')

        try:
            event = Event(name=event_name, event_organiser=event_organiser, event_held_on=event_held_on, event_desc=event_desc)
            event.save()
            messages.success(request, "Event Added Successfully!")
            return redirect("add_event")
        except:
            messages.error(request, "Failed to Add Event")
            return redirect("add_event")


def edit_event(request, event_id):
    event = Event.objects.get(id=event_id)
    context = {
        "event": event,
        "id": event_id
    }
    return render(request, "hod_template/edit_event_template.html", context)


def edit_event_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('manage_event')
    else:
        event_id = request.POST.get('event_id')
        event_name = request.POST.get('event_name')
        event_organiser = request.POST.get('event_organiser')
        event_held_on = request.POST.get('event_held_on')
        event_desc = request.POST.get('event_desc')

        try:
            event = Event.objects.get(id=event_id)
            event.event_name = event_name
            event.event_organiser = event_organiser
            event.event_held_on = event_held_on
            event.event_desc = event_desc
            event.save()

            messages.success(request, "Event Year Updated Successfully.")
            return redirect('/edit_event/'+event_id)
        except:
            messages.error(request, "Failed to Update Event Year.")
            return redirect('/edit_event/'+event_id)


def delete_event(request, event_id):
    event = Event.objects.get(id=event_id)
    try:
        event.delete()
        messages.success(request, "Event Deleted Successfully.")
        return redirect('manage_event')
    except:
        messages.error(request, "Failed to Delete Event.")
        return redirect('manage_event')


def add_student(request):
    form = AddStudentForm()
    context = {
        "form": form
    }
    return render(request, 'hod_template/add_student_template.html', context)




def add_student_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_student')
    else:
        form = AddStudentForm(request.POST, request.FILES)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            branch = form.cleaned_data['branch']

        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3)
            user.students.address = address
            user.students.branch = branch
            user.save()
            messages.success(request, "Student Added Successfully!")
            return redirect('add_student')
        except:
            messages.error(request, "Failed to Add Student!")
            return redirect('add_student')
        

def manage_student(request):
    students = Students.objects.all()
    context = {
        "students": students
    }
    return render(request, 'hod_template/manage_student_template.html', context)


def edit_student(request, student_id):
    # Adding Student ID into Event Variable
    student = Students.objects.get(admin=student_id)
    form = EditStudentForm()
    # Filling the form with Data from Database
    form.fields['email'].initial = student.admin.email
    form.fields['username'].initial = student.admin.username
    form.fields['first_name'].initial = student.admin.first_name
    form.fields['last_name'].initial = student.admin.last_name
    form.fields['address'].initial = student.address
    form.fields['branch'].initial = student.branch

    context = {
        "id": student_id,
        "username": student.admin.username,
        "form": form
    }
    return render(request, "hod_template/edit_student_template.html", context)


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        if student_id == None:
            return redirect('/manage_student')

        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']

        try:
            # First Update into Custom User Model
            user = CustomUser.objects.get(id=student_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            # Then Update Students Table
            student_model = Students.objects.get(admin=student_id)
            student_model.address = address
            student_model.branch = branch
            student_model.save()
    
            messages.success(request, "Student Updated Successfully!")
            return redirect('/edit_student/'+student_id)
        except:
            messages.error(request, "Failed to Uupdate Student.")
            return redirect('/edit_student/'+student_id)
       

def delete_student(request, student_id):
    student = Students.objects.get(admin=student_id)
    try:
        student.delete()
        messages.success(request, "Student Deleted Successfully.")
        return redirect('manage_student')
    except:
        messages.error(request, "Failed to Delete Student.")
        return redirect('manage_student')


def add_notice(request):
    context = {}
    return render(request, 'hod_template/add_notice_template.html', context)



def add_notice_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_notice')
    else:
        notice_name = request.POST.get('notice')
        notice_details = request.POST.get('notice_details')

        try:
            notice = Notices(notice_name=notice_name, notice_details=notice_details)
            notice.save()
            messages.success(request, "Notice Added Successfully!")
            return redirect('add_notice')
        except:
            messages.error(request, "Failed to Add Notice!")
            return redirect('add_notice')


def manage_notice(request):
    notices = Notices.objects.all()
    context = {
        "notices": notices
    }
    return render(request, 'hod_template/manage_notice_template.html', context)


def edit_notice(request, notice_id):
    notice = Notices.objects.get(id=notice_id)
    context = {
        "notice": notice,
        "id": notice_id
    }
    return render(request, 'hod_template/edit_notice_template.html', context)


def edit_notice_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method!")
    else:
        notice_id = request.POST.get('notice_id')
        notice_name = request.POST.get('notice_name')
        notice_details = request.POST.get('notice_details')

        try:
            notice = Notices.objects.get(id=notice_id)
            notice.notice_name = notice_name
            notice.notice_details = notice_details
            notice.save()

            messages.success(request, "Subject Updated Successfully.")
            # return redirect('/edit_notice/'+notice_id)
            return HttpResponseRedirect(reverse("edit_notice", kwargs={"notice_id":notice_id}))

        except:
            messages.error(request, "Failed to Update Subject.")
            return HttpResponseRedirect(reverse("edit_notice", kwargs={"notice_id":notice_id}))
            # return redirect('/edit_notice/'+notice_id)



def delete_notice(request, notice_id):
    notice = Notices.objects.get(id=notice_id)
    try:
        notice.delete()
        messages.success(request, "Subject Deleted Successfully.")
        return redirect('manage_notice')
    except:
        messages.error(request, "Failed to Delete Subject.")
        return redirect('manage_notice')


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)



def student_feedback_message(request):
    feedbacks = FeedBackStudent.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'hod_template/student_feedback_template.html', context)


@csrf_exempt
def student_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")



def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    context={
        "user": user
    }
    return render(request, 'hod_template/admin_profile.html', context)


def admin_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('admin_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('admin_profile')
    





def student_profile(requtest):
    pass



