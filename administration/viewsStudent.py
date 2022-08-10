from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .serializerStudent import ParentSerializer,StudentSerializer,StudentRegistrationSerializer
from .models import ParentsData,Student
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q

class StudentRegistrationView(ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentRegistrationSerializer

studentRegistrationView = StudentRegistrationView.as_view()

class StudentView(ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

studentView = StudentView.as_view()

class StudentCrudView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

studentCrudView = StudentCrudView.as_view()

class ParentView(ListCreateAPIView):
    queryset = ParentsData.objects.all()
    serializer_class = ParentSerializer

parentView = ParentView.as_view()

class ParentCrudView(RetrieveUpdateDestroyAPIView):
    queryset = ParentsData.objects.all()
    serializer_class = ParentSerializer

parentCrudView = ParentCrudView.as_view()

@api_view(['GET'])
def searchStudent(request, search):
    if request.method == "GET":
        students = Student.objects.filter(
            Q(first_name__contains = search) |
            Q(last_name__contains = search) |
            Q(given_name__contains = search) |
            Q(student_id__contains = search)
            )[:5]
        return Response(StudentSerializer(students,many=True).data)