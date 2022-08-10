from rest_framework import serializers
from .models import  Fee,IndividualClassFees
from .models import FeesPaymentRecord,StudentPaymentProfile
from .models import Fee,StaffPayment
from administration.serializersCommon import StudentClassSerializer,TermSerializer
from administration.serializerStudent import StudentSummarySerializer
from administration.models import Student, StudentClass,Term

        
class FeeSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source = 'student_class.name',read_only=True)
    class Meta:
        model = Fee
        fields = (
        'id','type','name','amount','class_name'
        )

class ChosenClassesSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()

class FeeRegistrationSerializer(serializers.ModelSerializer):
    fees = FeeSerializer(many=True,write_only=True)
    xclass = ChosenClassesSerializer(many=False,write_only=True)
    type = serializers.CharField(read_only = True)
    name = serializers.CharField(read_only = True)
    amount = serializers.DecimalField(read_only = True,max_digits=12,decimal_places=3)

    class Meta:
        model = Fee
        fields = (
            'id','type','name','amount','fees','xclass',
            )

    def create(self,validated_data):
        xclass = validated_data.pop("xclass")
        xfees = validated_data.pop("fees")
        x = StudentClass.objects.get(name = xclass['name'])

        for  f in xfees:
            qs_exists = Fee.objects.filter(student_class = x,name = f['name']).exists()
            if(qs_exists):
                fee = Fee.objects.filter(student_class = x,name = f['name']).first()
                fee.amount = f['amount']
                fee.save()
            else:
                fee = Fee.objects.create(
                        student_class = x, type = f['type'], 
                        name = f['name'], amount = f['amount'])
        class_fees = Fee.objects.filter(student_class = x).first()
        return class_fees

class ChosenTermSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()

class ChosenFeesSerializser(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()

class IndividualClassFeesRegistrationSerializer(serializers.ModelSerializer):
    xklass = ChosenClassesSerializer(many=False,write_only=True)
    xterm = ChosenTermSerializer(many=False,write_only=True)
    fees = ChosenFeesSerializser(many=True,write_only=True)
    student_class = StudentClassSerializer(many=False,read_only=True)
    key = serializers.CharField(source = 'id',read_only =True)
    class Meta:
        model = IndividualClassFees
        fields = (
        'id','xklass','xterm','term','fees','student_class','key',
        )

    def create(self,validated_data):
        xclass = validated_data.pop("xklass")
        xterm = validated_data.pop("xterm")
        xfees = validated_data.pop("fees")
        xKlass = StudentClass.objects.get(id = xclass['id']) 
        xTerm = Term.objects.get(id = xterm['id'])
        
        for f in xfees:
            fee = Fee.objects.get(id = f['id'])
            qs_exists = IndividualClassFees.objects.filter(student_class =xKlass,term = xTerm).exists()
            if(qs_exists):
                obj = IndividualClassFees.objects.filter(student_class =xKlass,term = xTerm).first()
            else:
                obj = IndividualClassFees.objects.create(student_class =xKlass,term = xTerm)
            
            obj.fees.add(fee)
        return  obj      
 

class IndividualClassFeesSerializer(serializers.ModelSerializer):
    key = serializers.CharField(source = 'id',read_only =True)
    class_name =  serializers.SerializerMethodField()
    term_name = serializers.SerializerMethodField()
    term_year = serializers.SerializerMethodField()
    term_start_date = serializers.SerializerMethodField()
    term_end_date = serializers.SerializerMethodField()
    fees = FeeSerializer(many=True,read_only=True)
    total_fees = serializers.SerializerMethodField()

    class Meta:
        model = IndividualClassFees
        fields = (
        'id','class_name',
        'term_name','term_year',
        'term_start_date','term_end_date',
        'fees','total_fees','key',
        )

    def get_class_name(self,obj):
        student_class = StudentClass.objects.get(id = obj.student_class.id)         
        return student_class.name

    def get_term_name(self,obj):
        term = Term.objects.get(id = obj.term.id)          
        return term.name 

    def get_term_year(self,obj):
        term = Term.objects.get(id = obj.term.id)          
        return term.academic_year 
    
    def get_term_start_date(self,obj):
        term = Term.objects.get(id = obj.term.id)          
        return term.start_date

    def get_term_end_date(self,obj):
        term = Term.objects.get(id = obj.term.id)          
        return term.end_date 

    def get_total_fees(self,obj):
        total = 0
        for f in obj.fees.all():
            total = total + f.amount
        return total

class StaffPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffPayment
        fields = "__all__"


class ChosenStudentSerializer(serializers.Serializer):
    id = serializers.CharField()
    student_id = serializers.CharField()

class FeesPaymentRegistrationSerializer(serializers.ModelSerializer):
    xstudent = ChosenStudentSerializer(many=False,write_only=True)
    xterm = ChosenTermSerializer(many=False,write_only=True)
    student = StudentSummarySerializer(many=False,read_only=True)
    term = TermSerializer(many=False,read_only=True)
    receipt_id = serializers.CharField(read_only = True)
    key = serializers.CharField(source = 'id',read_only =True)

    class Meta:
        model = FeesPaymentRecord
        fields = (
            'id','key','xstudent','xterm',
            'student','term','amount_paid','paid_by_name','paid_by_phone',
            'receipt_id','date_created'
        )

    def create(self,validated_data):
        xstudent = validated_data.pop("xstudent")
        xterm = validated_data.pop("xterm")

        xStudent = Student.objects.get(id = xstudent['id']) 
        xTerm = Term.objects.get(id = xterm['id'])

        record = FeesPaymentRecord.objects.create(
            student = xStudent,
            term = xTerm,
            **validated_data
        )
        
        qs_exists = StudentPaymentProfile.objects.filter(
            student =xStudent,
            term = xTerm).exists()

        if(qs_exists):
            obj = StudentPaymentProfile.objects.filter(student =xStudent,term = xTerm).first()
        else:
            obj = StudentPaymentProfile.objects.create(student =xStudent,term = xTerm)

        obj.fees_payment_record.add(record)
        return record 

class FeesPaymentSerializer(serializers.ModelSerializer):
    student = StudentSummarySerializer(many=False,read_only=True)
    term = TermSerializer(many=False,read_only=True)
    class_name = serializers.SerializerMethodField()
    term_class_fees = serializers.SerializerMethodField()
    term_class_fees_total = serializers.SerializerMethodField()
    term_student_fees_total_payment = serializers.SerializerMethodField()
    key = serializers.CharField(source = 'id',read_only =True)
    
    class Meta:
        model = FeesPaymentRecord
        fields = (
            'id','key','student','term',
            'amount_paid','paid_by_name',
            'paid_by_phone','receipt_id',
            'class_name','term_class_fees',
            'term_class_fees_total',
            'term_student_fees_total_payment',
            'date_created'
        )

    def get_class_name(self,obj):
        xclass = obj.student.student_class
        return xclass.name

    def get_term_class_fees(self,obj):
        class_fees = IndividualClassFees.objects.filter(term = obj.term.id,student_class=obj.student.student_class.id)
        fees = class_fees.first().fees.all()
        return FeeSerializer(fees,many=True).data
    
    def get_term_class_fees_total(self,obj):
        class_fees = IndividualClassFees.objects.filter(term = obj.term.id,student_class=obj.student.student_class.id)
        total = 0
        for f in class_fees.first().fees.all():
            total = total + f.amount
        return total

    def get_term_student_fees_total_payment(self,obj):
        records = FeesPaymentRecord.objects.filter(term = obj.term.id,student=obj.student.id)
        total = 0
        for f in records:
            total = total + f.amount_paid
        return total

class FeesPaymentRecordSerializer(serializers.ModelSerializer):
    receipt_id = serializers.CharField(read_only = True)
    amount_paid = serializers.CharField(read_only = True)
    paid_by_name = serializers.CharField(read_only = True)
    paid_by_phone = serializers.CharField(read_only = True)

    class Meta:
        model = FeesPaymentRecord
        fields = (
            'id','receipt_id','amount_paid',
            'paid_by_name','paid_by_phone',
            'date_created'
        )

class StudentPaymentProfileSerializer(serializers.ModelSerializer):
    student = StudentSummarySerializer(many=False,read_only=True)
    term = TermSerializer(many=False,read_only=True)
    fees_payment_record = FeesPaymentRecordSerializer(many  = True,read_only=True)

    class Meta:
        model = StudentPaymentProfile
        fields = ('id','student','term','fees_payment_record')
