from rest_framework.generics import ListAPIView, ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .serializersStaff import SalaryRegistrationSerializer,MonthlyAllowanceSerializer
from .serializersStaff import AddStaffMonthlyAllowanceSerializer,RemoveStaffMonthlyAllowanceSerializer
from .serializersStaff import StaffMonthlyAllowanceSerializer
from .models import Salary,MonthlyAllowance,StaffMonthlyAllowance

class MonthlyAllowanceView(ListCreateAPIView):
    queryset = MonthlyAllowance.objects.all()
    serializer_class = MonthlyAllowanceSerializer

monthlyAllowanceView = MonthlyAllowanceView.as_view()

class MonthlyAllowanceCrudView(RetrieveUpdateDestroyAPIView):
    queryset = MonthlyAllowance.objects.all()
    serializer_class = MonthlyAllowanceSerializer

monthlyAllowanceCrudView = MonthlyAllowanceCrudView.as_view()

class AddStaffMonthlyAllowanceView(ListCreateAPIView):
    queryset = StaffMonthlyAllowance.objects.all()
    serializer_class = AddStaffMonthlyAllowanceSerializer

addStaffMonthlyAllowanceView = AddStaffMonthlyAllowanceView.as_view()

class RemoveStaffMonthlyAllowanceView(ListCreateAPIView):
    queryset = StaffMonthlyAllowance.objects.all()
    serializer_class = RemoveStaffMonthlyAllowanceSerializer

removeStaffMonthlyAllowanceView = RemoveStaffMonthlyAllowanceView.as_view()

class StaffMonthlyAllowanceView(ListAPIView):
    queryset = StaffMonthlyAllowance.objects.all()
    serializer_class = StaffMonthlyAllowanceSerializer

staffMonthlyAllowanceView = StaffMonthlyAllowanceView.as_view()

class StaffMonthlyAllowanceCrudView(RetrieveUpdateDestroyAPIView):
    queryset = StaffMonthlyAllowance.objects.all()
    serializer_class = StaffMonthlyAllowanceSerializer

staffMonthlyAllowanceCrudView = StaffMonthlyAllowanceCrudView.as_view()

######

class SalaryRegistrationView(ListCreateAPIView):
    queryset = Salary.objects.all()
    serializer_class = SalaryRegistrationSerializer

salaryRegistrationView = SalaryRegistrationView.as_view()
