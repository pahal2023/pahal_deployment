from django.urls import path
from .import views
from .import views_teacher as views2
from .import views_admin as views3


urlpatterns = [
    path('', views.dashboard, name='home'),

    # views
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('error404/', views.error_page, name='error404'),
    

    # views2
    path('dashboard/profile/', views2.dashboard, name="dashboard"),
    path('dashboard/timetable/', views2.timetable, name="timetable"),
    path('dashboard/tasks/', views2.tasks, name="tasks"),

    path('dashboard/student-info/', views2.student_info, name="student_info"),
    path('dashboard/attendance/', views2.attendance, name="attendance"),
    # path('dashboard/performance/', views2.performance, name="performance"),
    path('dashboard/admission/',views2.admission,name="admission"),

    path('dashboard/volunteer-info/', views2.volunteer_info, name="volunteer_info"),
    path('dashboard/volunteer-enrolment/',views2.volunteer_enrolment,name="volunteer_enrolment"),

    path('dashboard/report-attendance/', views2.attendance_report, name="attendance_report"),
    # path('dashboard/report-progress/', views2.progress_repost, name="progress_report"),


    # views3
    path('dashboard/add-tasks/', views3.add_task, name="add_tasks"),

    # Volunteer management
    path('dashboard/volunteers-permission/', views3.all_volunteers, name='all_volunteers'),
    path('dashboard/volunteer/edit/<str:reg_no>', views3.edit_volunteer, name='edit_volunteer'),
    path('dashboard/volunteer/delete/<str:reg_no>', views3.delete_volunteer, name='delete_volunteer'),
    path('dashboard/volunteer/suspend/<str:reg_no>', views3.suspend_volunteer, name='suspend_volunteer'),
    path('dashboard/volunteer/reactivate/<str:reg_no>', views3.reactivate_volunteer, name='reactivate_volunteer'),

    # Applicant management
    path('dashboard/applicants/', views3.applicant_list, name='applicant_list'),
    path('dashboard/applicants/<str:reg_no>/', views3.applicant_detail, name='applicant_detail'),
    path('dashboard/applicants/<str:reg_no>/approve/', views3.approve_applicant, name='approve_applicant'),
    path('dashboard/applicants/<str:reg_no>/reject/', views3.reject_applicant, name='reject_applicant'),

]
