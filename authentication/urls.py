from django.urls import path
from  .views import basic_setup
from .views import users_list_create_view,permissions_list_create_view,groups_list_create_view
from .views import add_object_permissions_to_group_view,remove_object_permissions_from_group_view
from .views import add_user_to_group_view,remove_user_from_group_view
from .views import users_retrieve_update_destroy_view
from .views import content_type_list_view,contentTypePermissionView
from .views import groups_retrieve_update_delete_view, getuser, CustomTokenObtainPairView
from .views import groupCategoryListCreateView,staffRolesListCreateView
from .views import studentRolesListCreateView,teacherRolesListCreateView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    #Views Basic Setup
    path('setup/',basic_setup,name="basic_setup"),
    #Permissions And Content Types urls
    path('content-types/', content_type_list_view,name='contentTypes'),
    path('content-types/perms/', contentTypePermissionView,name='content-types-perms'),
    path('perms/', permissions_list_create_view,name='perms'),
    #Group urls
    path('groups/', groups_list_create_view,name='groups_list'),
    path('groups/edit/<int:pk>/', groups_retrieve_update_delete_view,name='group_retrieve_update_delete'),
    path('groups/add_object_perms/<int:pk>', add_object_permissions_to_group_view,name='remove_perms_group'),
    path('groups/remove_object_perms/<int:pk>', remove_object_permissions_from_group_view,name='remove_object_perms_group'),
    path('roles/', groupCategoryListCreateView,name='roles_list'),
    path('student/roles/', studentRolesListCreateView,name='student_roles_list'),
    path('teacher/roles/', teacherRolesListCreateView,name='teacher_roles_list'),
    path('staff/roles/', staffRolesListCreateView,name='staff_roles_list'),
    #User urls
    path('users/', users_list_create_view,name='users_list'),
    path('users/<int:pk>/', users_retrieve_update_destroy_view,name='user_retrieve_update_delete'),
    path('users/add_to_group/<int:pk>/', add_user_to_group_view,name='add_user_to_group'),
    path('users/remove_from_group/<int:pk>/', remove_user_from_group_view,name='remove_user_from_group'),

    #JWT Authotentcation
    path('api/token/access/', CustomTokenObtainPairView.as_view(),name="tkn"),
    path('api/token/refresh/',TokenRefreshView.as_view(),name='tkn2')

]