from django.urls import path
from.views import basic_setup
from .viewsCommon import studentClassView,studentClassCrudView,subjectUnitView
from .viewsCommon import subjectUnitCrudView,termView,termCrudView
from .viewsStaff import searchStaff, staffView,staffCrudView
from .viewsStaff import teachingStaffView,teachingStaffCrudView,nonTeachingStaffView,nonTeachingStaffCrudView
from .viewsStudent import studentView,studentCrudView,parentView,parentCrudView,studentRegistrationView,searchStudent

urlpatterns = [
    #Views Basic Setup
    path('setup/',basic_setup,name="basic_setup"),
    #Views Common
    path('terms/',termView,name="terms"),
    path('terms-crud/<int:pk>/',termCrudView,name="terms-crud"),
    path('classes/',studentClassView,name="classes"),
    path('classes-crud/<int:pk>/',studentClassCrudView,name="classes-crud"),
    path('subjects/',subjectUnitView,name="subjects"),
    path('subjects-crud/<int:pk>/',subjectUnitCrudView,name="subjects-crud"),
    #Views Staff
    path('staff/',staffView,name="staff"),
    path('staff-crud/<int:pk>/',staffCrudView,name="staff-crud"),
    path('teaching-staff/',teachingStaffView,name="teaching-staff"),
    path('teaching-staff-crud/<int:pk>/',teachingStaffCrudView,name="teaching-staff-crud"),
    path('staff-search/<str:search>/', searchStaff, name="staff-search"),
    path('non-teaching-staff/',nonTeachingStaffView,name="non-teaching-staff"),
    path('non-teaching-staff-crud/<int:pk>/',nonTeachingStaffCrudView,name="non-teaching-staff-crud"),
    #Views Student
    path('students/',studentView,name="students"),
    path('students/register/',studentRegistrationView,name="students-register"),
    path('students-crud/<int:pk>/',studentCrudView,name="students-crud"),
    path('students-search/<str:search>/', searchStudent, name="student-search"),
    path('parents/',parentView,name="parents"),
    path('parents-crud/<int:pk>/',parentCrudView,name="parents-crud"),
]