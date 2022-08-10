import re
from unicodedata import category
from django.db import models
from item.models import Category
from administration.models import Student,StudentClass,Staff,Term
from django.contrib.auth.models import User
from datetime import date
from decimal import Decimal
from mulumba.utils import random_string_generator
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Fee(models.Model):
    TYPE = [
        ("STANDARD","STANDARD"),
        ("FUNCTIONAL","FUNCTIONAL"),
        ("EXTRA","EXTRA"),
        ("DAMAGES","DAMAGES"),
        ("DEBT","DEBT"),
        ("PERSONAL","PERSONAL"),
        ("EMERGENCY","EMERGENCY"),
    ]
    type = models.CharField(choices=TYPE,max_length=100)
    name = models.CharField(max_length=255)
    student_class = models.ForeignKey(StudentClass,null = True,related_name="class_fee", on_delete=models.SET_NULL)
    amount = models.DecimalField(default = 0.0, max_digits=12,decimal_places=3)
    
    def __str__(self):
        return self.name
    

class IndividualClassFees(models.Model):
    student_class = models.ForeignKey(StudentClass,null = True,related_name="class_fees", on_delete=models.SET_NULL)
    term =models.ForeignKey(Term,null = True,on_delete=models.SET_NULL)
    fees = models.ManyToManyField(Fee)
    created_by = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)

class IndividualStudentFees(models.Model):
    student =models.ForeignKey(Student,related_name="student_fees",null = True,on_delete=models.SET_NULL)
    term =models.ForeignKey(Term,null = True,on_delete=models.SET_NULL)
    fees = models.ManyToManyField(Fee)
    created_by = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)

class IncomeType(models.Model):
    name = models.CharField(max_length=100,unique=True)

class Income(models.Model):
    term =models.ForeignKey(Term,null = True,on_delete=models.SET_NULL)
    # student_fees = models.ForeignKey(StudentFees,null=True,on_delete=models.SET_NULL)
    # students_per_class = models.IntegerField(null=True)
    # fees_per_class = models.DecimalField(max_digits=12, decimal_places=2,null=True)
    category = models.ForeignKey(IncomeType,null=True,on_delete=models.SET_NULL)
    budgetted_expenditure =models.DecimalField(max_digits=12, decimal_places=2,null=True)
    created_by = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_updated = models.DateTimeField(null=True,blank=True)

    def get_students_per_class(self):
        pass

    def get_amount_per_category(self):
        pass
    
    def get_total_income(self):
        pass

    def get_total_enrollment(self):
        pass

    def get_total_devt_income(self):
        pass

    def get_est_total_fees_collection(self):
        pass

    def get_surplus(self):
        pass

class Expenditure(models.Model):
    term =models.ForeignKey(Term,null = True,on_delete=models.SET_NULL)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    created_by = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_updated = models.DateTimeField(null=True,blank=True)

    def get_total(self):
        categories = self.category_set.all()
        total = 0
        for i in categories:
            total = total + i.get_category_total()
        return total


class Payment(models.Model):
    name = models.CharField(max_length=200,null=True,blank=True,)
    basic = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    allowance_amt = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    nssf_percent = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    advance_amt = models.DecimalField(max_digits=5, decimal_places=2,null=True)

    def __str__(self) -> str:
        return self.name

    def get_allowance_percent(self):
        pass

    def get_nssf_amout(self):
        pass

    def get_advance_percent(self):
        pass

    def get_total_deduction(self):
        pass

    def get_net_pay(self):
        pass    

class StaffPayment(models.Model):
    payment = models.ForeignKey(Payment,null=True,on_delete=models.SET_NULL)
    staff = models.ForeignKey(Staff,null=True,on_delete=models.SET_NULL)


class FeesPaymentRecord(models.Model):
    student = models.ForeignKey(Student,null=True,on_delete=models.SET_NULL)
    term = models.ForeignKey(Term,null=True,on_delete=models.SET_NULL)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=3,null=True)
    receipt_id = models.CharField(max_length=225,unique=True,blank=True,null=True)
    paid_by_name = models.CharField(max_length=225,unique=True,blank=True,null=True)
    paid_by_phone = models.CharField(max_length=225,unique=True,blank=True,null=True)
    created_by = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)

@receiver(pre_save, sender = FeesPaymentRecord)
def unique_receipt_id_generator(instance, *args, **kwargs):
    id = random_string_generator(size=7)
    id = "RT-" + id.upper()
    qs_exists = FeesPaymentRecord.objects.filter(receipt_id = id).exists()
    if(qs_exists):
        return unique_receipt_id_generator(instance, *args, **kwargs)
    else:
        instance.receipt_id = id 


class StudentPaymentProfile(models.Model):
    student = models.ForeignKey(Student,null=True,on_delete=models.SET_NULL)
    term = models.ForeignKey(Term,null=True,on_delete=models.SET_NULL)
    fees_payment_record = models.ManyToManyField(FeesPaymentRecord)


#Salaries

class PaymentPeriod(models.Model):
    term = models.ForeignKey(Term,null=True,on_delete=models.SET_NULL)
    month = models.IntegerField(null=True) # Year And Month Should Be Unique
    year = models.IntegerField(null=True)
    created_by = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)


class MonthlyAllowance(models.Model):
    name = models.CharField(max_length=255)
    amount =  models.DecimalField(default = 0.0, max_digits=12,decimal_places=3)
    is_approved = models.BooleanField(default=False)
    created_by = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)


class StaffMonthlyAllowance(models.Model):
    staff = models.ForeignKey(Staff,null=True,on_delete=models.SET_NULL)
    monthly_allowances = models.ManyToManyField(MonthlyAllowance)
    created_by = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)

    def get_total_allowances(self):
        all = self.monthly_allowances.all()
        total = 0
        for i in all:
            total = total + i.amount
        return total


class StaffMonthlyAdvance(models.Model):
    staff = models.ForeignKey(Staff,null=True,on_delete=models.SET_NULL)
    reason = models.CharField(max_length=255,unique=True)
    requested_amount =  models.DecimalField(default = 0.0, max_digits=12,decimal_places=3)
    issued_amount =  models.DecimalField(default = 0.0, max_digits=12,decimal_places=3)
    repayment_period = models.IntegerField(default = 1) #Months
    is_issued = models.BooleanField(default=False)
    created_by = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)

    def get_total_amount_paid(self):
        all = self.repayments.all()
        total = 0
        for i in all:
            total = i.amount_paid
        return total
    
    def get_total_no_of_months_paid(self):
        all = self.repayments.all()
        return all.count()
    
    def get_balance_per_repayment_months(self):
        total_amount_paid_so_far = self.get_total_amount_paid()
        total_no_of_months_paid_so_far = self.get_total_no_of_months_paid()
        amount_balance = self.issued_amount - total_amount_paid_so_far
        repayment_months_balance = self.repayment_period - total_no_of_months_paid_so_far
        if(repayment_months_balance == 0 and amount_balance == 0):
            return 0
        elif(amount_balance > 0 and repayment_months_balance <= 0):
            return amount_balance
        else:
            return amount_balance / repayment_months_balance

class MonthlyAdvanceRepayment(models.Model):
    staff = models.ForeignKey(Staff,null=True,on_delete=models.SET_NULL)
    monthly_advance = models.ForeignKey(StaffMonthlyAdvance,null=True, related_name="repayments",on_delete=models.SET_NULL)
    amount_paid =  models.DecimalField(default = 0.0, max_digits=12,decimal_places=3)
    payback_period = models.ForeignKey(PaymentPeriod,related_name="advance_requests",null=True,on_delete=models.SET_NULL)
    receipt_id = models.CharField(max_length=225,unique=True,blank=True,null=True)
    created_by = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    date_paid = models.DateTimeField(auto_now_add=True)


class AdvanceRequest(models.Model):
    staff = models.ForeignKey(Staff,null=True,on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(default = 0.0, max_digits=12,decimal_places=3)
    repayment_period = models.IntegerField(default = 1)
    is_approved = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    created_by = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)


class Salary(models.Model):
    staff = models.ForeignKey(Staff,null=True,on_delete=models.SET_NULL)
    basic_amount = models.DecimalField(default = 0.0, max_digits=12,decimal_places=3)
    nssf_percentage = models.DecimalField(default = 0.0, max_digits=12,decimal_places=3)

    def get_nssf_amount(self): 
        amt = (self.nssf_percentage / 100) * self.basic_amount
        return amt
    
    def get_normal_net_pay(self):
        nssf_amount = self.get_nssf_amount()
        return self.basic_amount - nssf_amount

class StaffSalary(models.Model):
    staff = models.ForeignKey(Staff,null=True,on_delete=models.SET_NULL)
    salary = models.ForeignKey(Salary,null=True,on_delete=models.SET_NULL)

    def get_allowances(self):
        data = StaffMonthlyAllowance.objects.filter(staff = self.staff)
        return data

    def get_advances(self):
        data = StaffMonthlyAdvance.objects.filter(staff = self.staff)
        return data



