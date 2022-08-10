from django.urls import path
from .viewsStudent import feesListView,feesCrudView,feeRegistrationView
from .viewsStudent import classFeesView,classFeesCrudView,classFeesRegistrationView
from .viewsStudent import feesPaymentRegistrationView,studentPaymentProfileView
from .viewsStudent import feesPaymentView,feesPaymentCrudView
# from .viewsStaff import allowancePaymentRecordRegistrationView,advancePaymentRecordRegistrationView
# from .viewsStaff import allowancePaymentRecordCrudView,advancePaymentRecordCrudView
# from .viewsStaff import allowancePaymentView,advancePaymentView
# from .viewsStaff import paymentPeriodAllowanceView,paymentPeriodAdvanceView
from .viewsStaff import salaryRegistrationView,monthlyAllowanceView,monthlyAllowanceCrudView
from .viewsStaff import addStaffMonthlyAllowanceView,removeStaffMonthlyAllowanceView
from .viewsStaff import staffMonthlyAllowanceView,staffMonthlyAllowanceCrudView

urlpatterns = [
    path('fees-register/',feeRegistrationView,name="fees-register"),
    path('fees-list/',feesListView,name="fees-list"),
    path('fees-crud/<int:pk>/',feesCrudView,name="fees-crud"),
    path('class-fees/register/',classFeesRegistrationView,name="fees-class-register"),
    path('class-fees/',classFeesView,name="fees-class"),
    path('class-fees-crud/<int:pk>/',classFeesCrudView,name="fees-class-crud"),
    path('fees-term-payment/',feesPaymentRegistrationView,name="fees-term-payment"),
    path('fees-term-payment-list/',feesPaymentView,name="fees-term-payment-list"),
    path('fees-term-payment-crud/<int:pk>/',feesPaymentCrudView,name="fees-term-payment-crud"),
    path('student=payment-profile/',studentPaymentProfileView,name="studentPaymentProfileView"),

    #Staff
    # path('staff-allowance-payment/list/',allowancePaymentView,name="staff-allowance-payment-list"),
    # path('staff-allowance-payment-record/add/',allowancePaymentRecordRegistrationView,name="staff-allowance-payment-record-add"),
    # path('staff-allowance-payment-record-crud/<int:pk>/',allowancePaymentRecordCrudView,name="staff-allowance-payment-record-crud"),
    # path('staff-advance-payment/list/',advancePaymentView,name="staff-advance-payment-list"),
    # path('staff-advance-payment-record/add/',advancePaymentRecordRegistrationView,name="staff-advance-payment-record-add"),
    # path('staff-advance-payment-record-crud/<int:pk>/',advancePaymentRecordCrudView,name="staff-advance-payment-record-crud"),
    # path('staff-payment-period-allowances/',paymentPeriodAllowanceView,name="staff-payment-period-allowances"),
    # path('staff-payment-period-advances/',paymentPeriodAdvanceView,name="staff-payment-period-advances"),
    path('monthly-allowances/',monthlyAllowanceView,name="monthly-allowances"),
    path('monthly-allowances-crud/<int:pk>/',monthlyAllowanceCrudView,name="monthly-allowances-crud"),
    path('staff-monthly-allowances/',addStaffMonthlyAllowanceView,name="staff-monthly-allowances"),
    path('staff-monthly-allowances-remove/',removeStaffMonthlyAllowanceView,name="staff-monthly-allowances-remove"),
    path('staff-monthly-allowances/list/',staffMonthlyAllowanceView,name="staff-monthly-allowances-list"),
    path('staff-monthly-allowances-crud/<int:pk>/',staffMonthlyAllowanceCrudView,name="staff-monthly-allowances-crud"),

    path('staff-salary-register/',salaryRegistrationView,name="staff-salary-register"),
]