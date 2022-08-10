from rest_framework.generics import ListAPIView, ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .serializerStaff import StaffSerializer,TeachingStaffSerializer,NonTeachingStaffSerializer
from .models import Staff
from django.contrib.auth.models import Group
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q

class StaffView(ListAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

staffView = StaffView.as_view()

class StaffCrudView(RetrieveUpdateDestroyAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

staffCrudView = StaffCrudView.as_view()

class TeachingStaffView(ListCreateAPIView):
    serializer_class = TeachingStaffSerializer

    def get_queryset(self):
        qs_exists = Group.objects.filter(name= "Teacher").exists()
        if(qs_exists):
            role = Group.objects.filter(name= "Teacher").first()
            data = Staff.objects.filter(roles=role)
            return(data)
        return Staff.objects.none()

teachingStaffView = TeachingStaffView.as_view()

class TeachingStaffCrudView(RetrieveUpdateDestroyAPIView):
    serializer_class = TeachingStaffSerializer

    def get_queryset(self):
        qs_exists = Group.objects.filter(name= "Teacher").exists()
        if(qs_exists):
            role = Group.objects.filter(name= "Teacher").first()
            data = Staff.objects.filter(roles=role)
            return(data)
        return Staff.objects.none()

teachingStaffCrudView = TeachingStaffCrudView.as_view()

class NonTeachingStaffView(ListCreateAPIView):
    serializer_class = NonTeachingStaffSerializer

    def get_queryset(self):
        qs_exists = Group.objects.filter(name= "Teacher").exists()
        if(qs_exists):           
            role = Group.objects.filter(name= "Teacher").first()
            return Staff.objects.exclude(roles = role)
        else:
            return Staff.objects.all()

nonTeachingStaffView = NonTeachingStaffView.as_view()

class NonTeachingStaffCrudView(RetrieveUpdateDestroyAPIView):
    serializer_class = NonTeachingStaffSerializer

    def get_queryset(self):
        qs_exists = Group.objects.filter(name= "Teacher").exists()
        if(qs_exists):           
            role = Group.objects.filter(name= "Teacher").first()
            return Staff.objects.exclude(roles = role)
        else:
            return Staff.objects.all()

nonTeachingStaffCrudView = NonTeachingStaffCrudView.as_view()

@api_view(['GET'])
def searchStaff(request, search):
    if request.method == "GET":
        staffs = Staff.objects.filter(
            Q(first_name__contains = search) |
            Q(last_name__contains = search) |
            Q(given_name__contains = search) |
            Q(staff_id__contains = search)
            )[:5]
        return Response(StaffSerializer(staffs,many=True).data)