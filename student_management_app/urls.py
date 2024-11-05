from django.contrib import admin
from django.urls import path, include
from . import views
from .import HodViews, StudentViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('contact', views.contact, name="contact"),
    path('login', views.loginUser, name="login"),
    path('logout_user', views.logout_user, name="logout_user"),
    path('registration', views.registration, name="registration"),
    path('doLogin', views.doLogin, name="doLogin"),
    path('doRegistration', views.doRegistration, name="doRegistration"),
    
      # URLS for Student
    path('student_home/', StudentViews.student_home, name="student_home"),
    path('view_notice/', StudentViews.view_notice, name="view_notice"),
    path('view_event/', StudentViews.view_event, name="view_event"),
    path('view_club/', StudentViews.view_club, name="view_club"),

    path('student_feedback/', StudentViews.student_feedback, name="student_feedback"),
    path('student_feedback_save/', StudentViews.student_feedback_save, name="student_feedback_save"),
    path('student_profile/', StudentViews.student_profile, name="student_profile"),
    path('student_profile_update/', StudentViews.student_profile_update, name="student_profile_update"),


     
    # URL for Admin
    path('admin_home/', HodViews.admin_home, name="admin_home"),
    path('add_club/', HodViews.add_club, name="add_club"),
    path('add_club_save/', HodViews.add_club_save, name="add_club_save"),
    path('manage_club/', HodViews.manage_club, name="manage_club"),
    path('edit_club/<club_id>/', HodViews.edit_club, name="edit_club"),
    path('edit_club_save/', HodViews.edit_club_save, name="edit_club_save"),
    path('delete_club/<club_id>/', HodViews.delete_club, name="delete_club"),
    path('manage_event/', HodViews.manage_event, name="manage_event"),
    path('add_event/', HodViews.add_event, name="add_event"),
    path('add_event_save/', HodViews.add_event_save, name="add_event_save"),
    path('edit_event/<event_id>', HodViews.edit_event, name="edit_event"),
    path('edit_event_save/', HodViews.edit_event_save, name="edit_event_save"),
    path('delete_event/<event_id>/', HodViews.delete_event, name="delete_event"),
    path('add_student/', HodViews.add_student, name="add_student"),
    path('add_student_save/', HodViews.add_student_save, name="add_student_save"),
    path('edit_student/<student_id>', HodViews.edit_student, name="edit_student"),
    path('edit_student_save/', HodViews.edit_student_save, name="edit_student_save"),
    path('manage_student/', HodViews.manage_student, name="manage_student"),
    path('delete_student/<student_id>/', HodViews.delete_student, name="delete_student"),
    path('add_notice/', HodViews.add_notice, name="add_notice"),
    path('add_notice_save/', HodViews.add_notice_save, name="add_notice_save"),
    path('manage_notice/', HodViews.manage_notice, name="manage_notice"),
    path('edit_notice/<notice_id>/', HodViews.edit_notice, name="edit_notice"),
    path('edit_notice_save/', HodViews.edit_notice_save, name="edit_notice_save"),
    path('delete_notice/<notice_id>/', HodViews.delete_notice, name="delete_notice"),
    path('check_email_exist/', HodViews.check_email_exist, name="check_email_exist"),
    path('check_username_exist/', HodViews.check_username_exist, name="check_username_exist"),
    path('student_feedback_message/', HodViews.student_feedback_message, name="student_feedback_message"),
    path('student_feedback_message_reply/', HodViews.student_feedback_message_reply, name="student_feedback_message_reply"),
    path('admin_profile/', HodViews.admin_profile, name="admin_profile"),
    path('admin_profile_update/', HodViews.admin_profile_update, name="admin_profile_update"),
    

]



