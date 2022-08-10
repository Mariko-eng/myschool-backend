from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .serializersCommon import StudentClassSerializer,SubjectUnitSerializer,TermSerializer
from .models import StudentClass,SubjectUnit,Term

class TermView(ListCreateAPIView):
    queryset = Term.objects.all()
    serializer_class = TermSerializer

termView = TermView.as_view()

class TermCrudView(RetrieveUpdateDestroyAPIView):
    queryset = Term.objects.all()
    serializer_class = TermSerializer

termCrudView = TermCrudView.as_view()

class StudentClassView(ListCreateAPIView):
    queryset = StudentClass.objects.all()
    serializer_class = StudentClassSerializer

studentClassView = StudentClassView.as_view()

class StudentClassCrudView(RetrieveUpdateDestroyAPIView):
    queryset = StudentClass.objects.all()
    serializer_class = StudentClassSerializer

studentClassCrudView = StudentClassCrudView.as_view()

class SubjectUnitView(ListCreateAPIView):
    queryset = SubjectUnit.objects.all()
    serializer_class = SubjectUnitSerializer

subjectUnitView = SubjectUnitView.as_view()

class SubjectUnitCrudView(RetrieveUpdateDestroyAPIView):
    queryset = SubjectUnit.objects.all()
    serializer_class = SubjectUnitSerializer

subjectUnitCrudView = SubjectUnitCrudView.as_view()

