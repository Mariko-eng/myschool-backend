from rest_framework.generics import ListAPIView, ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .serializersStudent import FeeSerializer, FeeRegistrationSerializer
from .serializersStudent import IndividualClassFeesRegistrationSerializer,IndividualClassFeesSerializer
from .serializersStudent import FeesPaymentRegistrationSerializer,FeesPaymentSerializer
from .serializersStudent import StudentPaymentProfileSerializer
from .models import Fee,IndividualClassFees,FeesPaymentRecord,StudentPaymentProfile

class FeeRegistrationView(ListCreateAPIView):
    queryset = Fee.objects.all()
    serializer_class = FeeRegistrationSerializer

feeRegistrationView = FeeRegistrationView.as_view()

class FeesListView(ListAPIView):
    queryset = Fee.objects.all()
    serializer_class = FeeSerializer

feesListView = FeesListView.as_view()

class FeesCrudView(RetrieveUpdateDestroyAPIView):
    queryset = Fee.objects.all()
    serializer_class = FeeSerializer

feesCrudView = FeesCrudView.as_view()

class ClassFeesRegistrationView(ListCreateAPIView):
    queryset = IndividualClassFees.objects.all()
    serializer_class = IndividualClassFeesRegistrationSerializer

classFeesRegistrationView = ClassFeesRegistrationView.as_view()

class ClassFeesView(ListCreateAPIView):
    queryset = IndividualClassFees.objects.all()
    serializer_class = IndividualClassFeesSerializer

classFeesView = ClassFeesView.as_view()

class ClassFeesCrudView(RetrieveUpdateDestroyAPIView):
    queryset = IndividualClassFees.objects.all()
    serializer_class = IndividualClassFeesSerializer

classFeesCrudView = ClassFeesCrudView.as_view()

class FeesPaymentRegistrationView(ListCreateAPIView):
    queryset = FeesPaymentRecord.objects.all()
    serializer_class = FeesPaymentRegistrationSerializer

feesPaymentRegistrationView = FeesPaymentRegistrationView.as_view()

class FeesPaymentView(ListAPIView):
    queryset = FeesPaymentRecord.objects.all()
    serializer_class = FeesPaymentSerializer

feesPaymentView = FeesPaymentView.as_view()

class FeesPaymentCrudView(RetrieveUpdateDestroyAPIView):
    queryset = FeesPaymentRecord.objects.all()
    serializer_class = FeesPaymentSerializer

feesPaymentCrudView = FeesPaymentCrudView.as_view()

class StudentPaymentProfileView(ListAPIView):
    queryset = StudentPaymentProfile.objects.all()
    serializer_class = StudentPaymentProfileSerializer

studentPaymentProfileView = StudentPaymentProfileView.as_view()

