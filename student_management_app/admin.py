from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AdminHOD, Clubs, Event, Notices, Students, FeedBackStudent, NotificationStudent

# Register your models here.
class UserModel(UserAdmin):
    pass


admin.site.register(CustomUser, UserModel)

admin.site.register(AdminHOD)
admin.site.register(Clubs)
admin.site.register(Event)
admin.site.register(Notices)
admin.site.register(Students)
admin.site.register(FeedBackStudent)
admin.site.register(NotificationStudent)


