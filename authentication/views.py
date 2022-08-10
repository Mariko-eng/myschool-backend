from rest_framework.response import Response
from .serializers import UserSerializer, GroupSerializer,PermissionSerializer
from .serializers import ContentTypeSerializer, ContentTypePermissionSerializer
from .serializers import AddObjectPermissionsToGroupSerializer,RemoveObjectPermissionsFromGroupSerializer
from .serializers import AddUserToGroupSerializer,RemoveUserFromGroupSerializer
from django.contrib.auth.models import User, Permission, Group
from rest_framework import generics
from rest_framework.decorators import api_view,permission_classes
from rest_framework import permissions
from mulumba.pagination import StandardResultsSetPagination
from rest_framework_simplejwt.views import TokenObtainPairView
from .jwtAuth import CustomTokenObtainSerializer
from django.contrib.contenttypes.models import ContentType
from .models import GroupCategory
from .serializers import GroupCategorySerializer

class ContentTypeView(generics.ListAPIView):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer

content_type_list_view = ContentTypeView.as_view()

class ContentTypePermissionView(generics.ListAPIView):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypePermissionSerializer

contentTypePermissionView = ContentTypePermissionView.as_view()

class PermissionsView(generics.ListCreateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    # pagination_class = StandardResultsSetPagination

permissions_list_create_view = PermissionsView.as_view()

class GroupsListCreateView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def perform_create(self, serializer):
        return super().perform_create(serializer)

groups_list_create_view = GroupsListCreateView.as_view()

class StudentRolesListCreateView(generics.ListCreateAPIView):
    serializer_class = GroupCategorySerializer

    def get_queryset(self):
        qs_exists = GroupCategory.objects.filter(name = "Student").exists()
        if(qs_exists):
            qs = GroupCategory.objects.filter(name = "Student")
            return qs
        else:
            return GroupCategory.objects.none()
    
studentRolesListCreateView = StudentRolesListCreateView.as_view()

class TeacherRolesListCreateView(generics.ListCreateAPIView):
    serializer_class = GroupCategorySerializer

    def get_queryset(self):
        qs_exists = GroupCategory.objects.filter(name = "Teacher").exists()
        if(qs_exists):
            qs = GroupCategory.objects.filter(name = "Teacher")
            return qs
        else:
            return GroupCategory.objects.none()

teacherRolesListCreateView = TeacherRolesListCreateView.as_view()

class StaffRolesListCreateView(generics.ListCreateAPIView):
    serializer_class = GroupCategorySerializer

    def get_queryset(self):
        qs_exists = GroupCategory.objects.filter(name = "Staff").exists()
        if(qs_exists):
            qs = GroupCategory.objects.filter(name = "Staff")
            return qs
        else:
            return GroupCategory.objects.none()

staffRolesListCreateView = StaffRolesListCreateView.as_view()

class GroupCategoryListCreateView(generics.ListCreateAPIView):
    queryset = GroupCategory.objects.all()
    serializer_class = GroupCategorySerializer

groupCategoryListCreateView = GroupCategoryListCreateView.as_view()

class AddObjectPermissionsToGroupView(generics.UpdateAPIView):
    queryset = Group.objects.all()
    serializer_class = AddObjectPermissionsToGroupSerializer

add_object_permissions_to_group_view = AddObjectPermissionsToGroupView.as_view()

class RemoveObjectPermissionsFromGroupView(generics.UpdateAPIView):
    queryset = Group.objects.all()
    serializer_class = RemoveObjectPermissionsFromGroupSerializer

remove_object_permissions_from_group_view = RemoveObjectPermissionsFromGroupView.as_view()

class AddUserToGroupView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = AddUserToGroupSerializer

add_user_to_group_view = AddUserToGroupView.as_view()

class RemoveUserFromGroupView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = RemoveUserFromGroupSerializer

remove_user_from_group_view = RemoveUserFromGroupView.as_view()

class GroupsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    # lookup_field = 'pk'
    # lookup_url_kwarg = 'pk'

groups_retrieve_update_delete_view = GroupsRetrieveUpdateDestroyView.as_view()

class UsersView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def get_queryset(self):
    #     users = User.objects.filter(is_active=True)
    #     return users;
    
    # def list(self, request, *args, **kwargs):
    #      users = User.objects.filter(is_active=True)
    #      serializer =  UserSerializer(users,many=True)
    #      return Response(serializer.data);


users_list_create_view = UsersView.as_view()

class UsersRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

users_retrieve_update_destroy_view = UsersRetrieveUpdateDestroyView.as_view()

    # def perform_destroy(self, instance):
    #     return super().perform_destroy(instance)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getuser(request):
    user = request.user
    # u = User.objects.get(username='van')
    s = UserSerializer(user,many= False)
    return Response(s.data)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer

@api_view(['GET'])
def basic_setup(request):
    student_roles = [
           "Student","Class Monitor","Head Prefect",
           "Asst Head Prefect","Prefect",           
    ]
    teacher_roles = [
        "Teacher","Class Teacher","Head Of Department",
        "Sciences Teacher","Arts Teacher",
    ]
    non_teacher_roles = [
           "Accountant","Store Keeper","Casual Staff",
           "Cooker","Cleaner","Gate-Keeeper",
           "Staff Admin","Administrative Board",
           "Headmaster","Deputy-Headmaster",
           "secretary","Accountant",
    ]
    if request.method == "GET":
        #Sutdent
        qs1_exists = GroupCategory.objects.filter(name = "Student").exists()
        if(qs1_exists):
            student_role = GroupCategory.objects.get(name = "Student")
        else:
            student_role = GroupCategory.objects.create(name= "Student")

        for group in student_roles:
            qs2_exists = Group.objects.filter(name = group).exists()
            if(qs2_exists):
                role = Group.objects.get(name = group)
            else:
                role = Group.objects.create(name= group)
            student_role.groups.add(role)

        #Teacher
        qs1_exists = GroupCategory.objects.filter(name = "Teacher").exists()
        if(qs1_exists):
            teacher_role = GroupCategory.objects.get(name = "Teacher")
        else:
            teacher_role = GroupCategory.objects.create(name= "Teacher")

        for group in teacher_roles:
            qs2_exists = Group.objects.filter(name = group).exists()
            if(qs2_exists):
                role = Group.objects.get(name = group)
            else:
                role = Group.objects.create(name= group)
            teacher_role.groups.add(role)
            
        #Staff
        qs1_exists = GroupCategory.objects.filter(name = "Staff").exists()
        if(qs1_exists):
            non_teacher_role = GroupCategory.objects.get(name = "Staff")
        else:
            non_teacher_role = GroupCategory.objects.create(name= "Staff")

        for group in non_teacher_roles:
            qs2_exists = Group.objects.filter(name = group).exists()
            if(qs2_exists):
                role = Group.objects.get(name = group)
            else:
                role = Group.objects.create(name= group)
            non_teacher_role.groups.add(role)

    return Response({"data": "Successful"})


