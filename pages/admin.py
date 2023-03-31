from django.contrib import admin
from .models import Student, Team, Room, Review, TeamReviewRoom, BusinessSystem, StudentReviewScore, StudentReviewAttendance, Feedback, AppImage
from import_export.admin import ImportExportModelAdmin
from django.utils.safestring import mark_safe

admin.site.site_header = 'KL CSE-H Learnathon/Hackathon Administration'
admin.site.site_title = 'KL CSE-H Learnathon/Hackathon Administration'

admin.site.register(AppImage)

# Register your models here.
@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    search_fields = ('registration_no', )
    list_filter = ('team__name', 'team__business_system', )
    list_display = ('registration_no', 'attendance')
    pass

@admin.register(Team)
class TeamAdmin(ImportExportModelAdmin):
    search_fields = ('name', )
    list_filter = ('business_system', 'course', )
    pass

@admin.register(Room)
class RoomAdmin(ImportExportModelAdmin):
    list_filter = ('floor', )
    pass

@admin.register(Review)
class ReviewAdmin(ImportExportModelAdmin):
    list_display = ('number', 'date_of_review', 'time_of_review', 'attendance_open', 'scoring_open', )
    list_editable = ('attendance_open', 'scoring_open', )
    ordering = ('number', 'date_of_review', 'time_of_review', )
    pass

@admin.register(TeamReviewRoom)
class TeamReviewRoomAdmin(ImportExportModelAdmin):
    search_fields = ('team_name', 'review__number', )
    list_filter = ('team__course', 'team__business_system')
    pass

@admin.register(BusinessSystem)
class BusinessSystemAdmin(ImportExportModelAdmin):
    search_fields = ('name', )
    pass

@admin.register(StudentReviewAttendance)
class StudentReviewAttendance(ImportExportModelAdmin):
    search_fields = ('student__registration_no', )
    list_filter = ('student__team__name', 'review__number', 'student__team__business_system', )
    list_display = ('student', 'review', 'absent', )
    list_editable = ('absent', )
    ordering = ('student__registration_no', 'review__number', )
    pass

@admin.register(StudentReviewScore)
class StudentReviewScoreAdmin(ImportExportModelAdmin):
    search_fields = ('student__registration_no', )
    list_filter = ('student__team__name', 'review__number', 'student__team__business_system', )
    list_display = ('student', 'review', 'score', 'comments', )
    ordering = ('student__registration_no', 'review__number', )

@admin.register(Feedback)
class FeedbackAdmin(ImportExportModelAdmin):
    list_filter = ('issue_type', 'resolved')
    search_fields = ('issue', 'issue_type', 'registration_no', )
    list_display = ('id', 'issue_f', 'issue_type', 'resolved', )
    ordering = ('-complaint_raised_time', )

    def issue_f(self, obj):
        link = '<a href="%s/change/">%s</a>' % (obj.id, obj.issue)
        return mark_safe(link)
    pass

