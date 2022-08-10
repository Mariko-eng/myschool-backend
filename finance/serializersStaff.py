from dataclasses import fields
from rest_framework import serializers
from administration.serializersCommon import StudentClassSerializer,TermSerializer
from administration.serializerStudent import StudentSummarySerializer
from administration.models import Student, StudentClass,Term,Staff
from .models import PaymentPeriod
from .models import Salary ,StaffSalary,MonthlyAllowance,StaffMonthlyAllowance
from administration.serializerStaff import StaffSerializer

class PaymentPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentPeriod
        fields = ('id','term','month','year',)

class StaffBriefDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = (
            'id','user',
            'staff_id',
            'first_name', 'last_name','given_name',
            'date_of_birth', 'gender','phone_number','email',
            'is_teacher',
           )

class MonthlyAllowanceSerializer(serializers.ModelSerializer):
    is_approved = serializers.BooleanField(read_only=True)
    key = serializers.CharField(source="id", read_only=True)
    class Meta:
        model = MonthlyAllowance
        fields = (
            'id','name','amount','is_approved','key',
        )

    def create(self,validated_data):
        name = validated_data.pop("name")
        amount = validated_data.pop("amount")
        qs_exists = MonthlyAllowance.objects.filter(name= name.capitalize(),amount = amount).exists()
        if(qs_exists):
            instance = MonthlyAllowance.objects.filter(name= name.capitalize(),amount = amount).first()
        else:    
            instance = MonthlyAllowance.objects.create(name=name.capitalize(),amount = amount)
        
        return instance

class ChosenMonthlyAllowanceSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()

class AddStaffMonthlyAllowanceSerializer(serializers.ModelSerializer):
    staff_id = serializers.CharField(write_only=True)
    allowances = ChosenMonthlyAllowanceSerializer(many=True, write_only=True)
    staff = serializers.CharField(read_only=True)
    monthly_allowances = MonthlyAllowanceSerializer(many=True,read_only=True)
    class Meta:
        model = StaffMonthlyAllowance
        fields = (
            'id','staff_id','allowances','staff','monthly_allowances',
        )

    def create(self,validated_data):
        staff_id = validated_data.pop("staff_id")
        allowances = validated_data.pop("allowances")
        staff = Staff.objects.get(id = staff_id)

        exists = StaffMonthlyAllowance.objects.filter(staff = staff).exists()
        if(exists):
            instance = StaffMonthlyAllowance.objects.filter(staff = staff).first()
        else:
            instance = StaffMonthlyAllowance.objects.create(staff = staff)

        for i in allowances:
            allowance = MonthlyAllowance.objects.get(id = i['id'])
            instance.monthly_allowances.add(allowance)

        return instance


class RemoveStaffMonthlyAllowanceSerializer(serializers.ModelSerializer):
    staff_id = serializers.CharField(write_only=True)
    x_allowance = ChosenMonthlyAllowanceSerializer(many=False, write_only=True)
    staff = serializers.CharField(read_only=True)
    monthly_allowances = MonthlyAllowanceSerializer(many=True,read_only=True)
    class Meta:
        model = StaffMonthlyAllowance
        fields = (
            'id','staff_id','x_allowance','staff','monthly_allowances',
        )

    def create(self,validated_data):
        staff_id = validated_data.pop("staff_id")
        xallowance = validated_data.pop("x_allowance")
        staff = Staff.objects.get(id = staff_id)

        exists = StaffMonthlyAllowance.objects.filter(staff = staff).exists()
        if(exists):
            instance = StaffMonthlyAllowance.objects.filter(staff = staff).first()
        else:
            instance = StaffMonthlyAllowance.objects.create(staff = staff)

        allowance = MonthlyAllowance.objects.get(id = xallowance['id'])
        instance.monthly_allowances.remove(allowance)
        return instance


class StaffMonthlyAllowanceSerializer(serializers.ModelSerializer):
    staff = StaffBriefDetailSerializer(many=False,read_only=True)
    monthly_allowances = MonthlyAllowanceSerializer(many=True,read_only=True)
    class Meta:
        model = StaffMonthlyAllowance
        fields = (
            'id','staff','monthly_allowances','get_total_allowances',
        )

# class AllowancePaymentRecordSerializer(serializers.ModelSerializer):
#     staff = StaffBriefDetailSerializer(many = False,read_only=True)
#     acknowlegement_id = serializers.CharField(read_only=True)
#     non_contractual_payment_period = PaymentPeriodSerializer(many = False,read_only=True)
#     class Meta:
#         model = AllowancePaymentRecord
#         fields = (
#             'id','name','amount',
#             'staff','acknowlegement_id','is_contractual',
#             'non_contractual_payment_period','date_created'
#         )

# class AllowancePaymentRecordRegistrationSerializer(serializers.ModelSerializer):
#     staff_id = serializers.CharField(write_only=True)
#     term_id = serializers.CharField(write_only=True)
#     month = serializers.IntegerField(write_only=True)
#     year = serializers.IntegerField(write_only=True)

#     class Meta:
#         model = AllowancePaymentRecord
#         fields = (
#             'id','staff_id','term_id','month','year','name',
#             'amount','staff','acknowlegement_id','is_contractual',
#             'non_contractual_payment_period','date_created'
#         )
        
#     def create(self,validated_data):
#         staff_id = validated_data.pop("staff_id")
#         term_id = validated_data.pop("term_id")
#         month = validated_data.pop("month")
#         year = validated_data.pop("year")
#         is_contractual = validated_data.pop("is_contractual")
#         name = validated_data.pop("name")
#         amount = validated_data.pop("amount")

#         staff = Staff.objects.get(id = staff_id)

#         if(is_contractual):
#             qs_exists = AllowancePaymentRecord.objects.filter(
#                 staff = staff,
#                 is_contractual= True,
#                 name =name.capitalize(),
#             ).exists()
#             if(qs_exists):
#                 record = AllowancePaymentRecord.objects.filter(
#                     staff = staff,is_contractual= True,name =name.capitalize()).first()
#                 record.amount = amount
#                 record.save()
#             else:    
#                 record = AllowancePaymentRecord.objects.create(
#                     staff = staff,is_contractual= True,
#                     name =name.capitalize(),
#                     amount= amount)
            
#             if(AllowancePayment.objects.filter(staff = staff).exists()):
#                 allowancePayment = AllowancePayment.objects.filter(staff = staff).first()
#             else:
#                 allowancePayment = AllowancePayment.objects.create(staff = staff)
            
#             allowancePayment.allowance_payments.add(record)     
#             return record
#         else:
#             term = Term.objects.get(id = term_id)
#             qs_exists = PaymentPeriod.objects.filter(term = term, month = month, year= year).exists()
#             if(qs_exists):
#                 period = PaymentPeriod.objects.filter(term = term, month = month, year= year).first()
#             else:
#                 period = PaymentPeriod.objects.create(term = term, month = month, year= year)
                
#             record = AllowancePaymentRecord.objects.create(
#                 staff = staff,
#                 is_contractual= False,
#                 non_contractual_payment_period = period,
#                 name =name.capitalize(),
#                 amount= amount)
            
#             if(AllowancePayment.objects.filter(staff = staff,payment_period= period).exists()):
#                 allowancePayment = AllowancePayment.objects.filter(staff = staff,payment_period= period).first()
#             else:
#                 allowancePayment = AllowancePayment.objects.create(staff = staff,payment_period= period)
            
#             allowancePayment.allowance_payments.add(record)
#             return record


# class AllowancePaymentSerializer(serializers.ModelSerializer):
#     allowance_payments = AllowancePaymentRecordSerializer(many = True,read_only=True)
#     total_non_contractual = serializers.SerializerMethodField()

#     class Meta:
#         model = AllowancePayment
#         fields = (
#             'id','staff',
#             'payment_period','allowance_payments',
#             'get_month_period','get_year_period',
#             'get_allowance_payments_per_period_per_staff',
#             'total_non_contractual'
#         )

#     def get_total_non_contractual(self,obj):
#         total = 0
#         all =  AllowancePaymentRecord.objects.filter(staff= obj.staff.id)
#         for i in all:
#             if(i.is_contractual):
#                 total = total + i.amount
#         return total


# class AdvancePaymentRecordSerializer(serializers.ModelSerializer):
#     staff_PK = serializers.CharField(source = 'staff.id',read_only=True)
#     staff_ID = serializers.CharField(source = 'staff.staff_id',read_only=True)
#     staff_phone = serializers.CharField(source = 'staff.phone_number',read_only=True)
#     acknowlegement_id = serializers.CharField(read_only=True)
#     payment_period_month = serializers.CharField(source = 'payment_period.month',read_only=True)
#     payment_period_year = serializers.CharField(source = 'payment_period.year',read_only=True)
#     payment_period_term = serializers.SerializerMethodField()

#     class Meta:
#         model = AdvancePaymentRecord
#         fields = (
#             'id','name','amount',
#             'staff_PK','staff_ID','staff_phone',
#             'acknowlegement_id','payment_period',
#             'payment_period_month','payment_period_year',
#             'payment_period_term','date_created'
#         )

#     def get_payment_period_term(self,obj):
#         return obj.payment_period.term.name


# class AdvancePaymentRecordRegistrationSerializer(serializers.ModelSerializer):
#     staff_id = serializers.CharField(write_only=True)
#     term_id = serializers.CharField(write_only=True)
#     month = serializers.IntegerField(write_only=True)
#     year = serializers.IntegerField(write_only=True)
#     staff_PK = serializers.CharField(source = 'staff.id',read_only=True)
#     staff_ID = serializers.CharField(source = 'staff.staff_id',read_only=True)
#     staff_phone = serializers.CharField(source = 'staff.phone_number',read_only=True)
#     acknowlegement_id = serializers.CharField(read_only=True)
#     payment_period_month = serializers.CharField(source = 'payment_period.month',read_only=True)
#     payment_period_year = serializers.CharField(source = 'payment_period.year',read_only=True)
#     payment_period_term = serializers.SerializerMethodField()

#     class Meta:
#         model = AdvancePaymentRecord
#         fields = (
#             'id','staff_id','term_id',
#             'month','year','name','amount',
#             'staff_PK','staff_ID','staff_phone',
#             'acknowlegement_id','payment_period',
#             'payment_period_month','payment_period_year',
#             'payment_period_term','date_created'
#         )
    
#     def create(self,validated_data):
#         staff_id = validated_data.pop("staff_id")
#         term_id = validated_data.pop("term_id")
#         month = validated_data.pop("month")
#         year = validated_data.pop("year")
#         name = validated_data.pop("name")
#         amount = validated_data.pop("amount")

#         staff = Staff.objects.get(id = staff_id)

#         term = Term.objects.get(id = term_id)
#         qs_exists = PaymentPeriod.objects.filter(term = term, month = month, year= year).exists()
#         if(qs_exists):
#             period = PaymentPeriod.objects.filter(term = term, month = month, year= year).first()
#         else:
#             period = PaymentPeriod.objects.create(term = term, month = month, year= year)
                
#         record = AdvancePaymentRecord.objects.create(
#             staff = staff,
#             payment_period = period,
#             name = name.capitalize(),
#             amount = amount)

#         if(AdvancePayment.objects.filter(staff = staff,payment_period= period).exists()):
#             advancePayment = AdvancePayment.objects.filter(staff = staff,payment_period= period).first()
#         else:
#             advancePayment = AdvancePayment.objects.create(staff = staff,payment_period= period)
            
#         advancePayment.advance_payments.add(record)
#         return record

#     def get_payment_period_term(self,obj):
#         return obj.payment_period.term.name


# class AdvancePaymentSerializer(serializers.ModelSerializer):  
#     advance_payments = AdvancePaymentRecordSerializer(many = True,read_only=True)

#     class Meta:
#         model = AdvancePayment
#         fields = (
#             'id','staff','payment_period','advance_payments',
#             'get_month_period','get_year_period','get_term_period',
#             'get_advance_payments_per_period_per_staff',
#         )

# class PaymentPeriodAllowanceSerialiser(serializers.ModelSerializer):
#     allowances = AllowancePaymentRecordSerializer(many = True)
#     class Meta:
#         model = PaymentPeriod
#         fields = (
#             'id','month','year','allowances'
#         )

# class PaymentPeriodAdvanceSerialiser(serializers.ModelSerializer):
#     advances = AdvancePaymentRecordSerializer(many = True)
#     class Meta:
#         model = PaymentPeriod
#         fields = (
#             'id','month','year','advances',
#         )



class SalaryRegistrationSerializer(serializers.ModelSerializer):
    staff_id = serializers.CharField(write_only=True)
    class Meta:
        model = Salary
        fields = ('id','staff_id','basic_amount','nssf_percentage')

    def create(self,validated_data):
        staff_id = validated_data.pop("staff_id")
        basic_amount = validated_data.pop("basic_amount")
        nssf_percentage = validated_data.pop("nssf_percentage")
        staff = Staff.objects.get(id = staff_id)
        qs_exists = Salary.objects.filter(staff = staff).exists()
        if(qs_exists):
            salary= Salary.objects.filter(staff = staff).first()
            salary.basic_amount= basic_amount
            salary.nssf_percentage =nssf_percentage
            salary.save()
        else:
            salary= Salary.objects.create(
                staff = staff,
                basic_amount = basic_amount,
                nssf_percentage = nssf_percentage)
        return salary

class SalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = ('id','staff_id','basic_amount','nssf_percentage')

class StaffSalarySerializer(serializers.ModelSerializer): 
    class Meta:
        model = StaffSalary
        fields = ('id','staff','salary','allowance_payment','advance_Payment',)

