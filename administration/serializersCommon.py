import re
from .models import StudentClass,SubjectUnit,Term,Student
from finance.models import Fee,IndividualClassFees
from rest_framework import serializers

class TermSerializer(serializers.ModelSerializer):
    total_fees = serializers.SerializerMethodField()
    class Meta:
        model = Term
        fields = (
            'id','name','start_date','end_date','academic_year','date_created','total_fees'

        )

    def create(self,validated_data):
        yr = validated_data.pop('academic_year')
        name = validated_data.pop('name')
        start_date = validated_data.pop('start_date')
        end_date = validated_data.pop('end_date')

        qs_exists = Term.objects.filter(academic_year = yr,name=name).exists()
        if(qs_exists):
            obj = Term.objects.filter(academic_year = yr,name=name).first()
            obj.start_date = start_date
            obj.end_date = end_date
            obj.save()
            return obj
        else:
            obj = Term.objects.create(
                name=name,
                start_date =start_date,
                end_date = end_date,
                academic_year = yr)
            return obj
    
    def get_total_fees(self,obj):
        qs_exists = IndividualClassFees.objects.filter(term=obj.id).exists()
        total = 0
        if(qs_exists):
            term_fees = IndividualClassFees.objects.filter(term=obj.id).first()
            for f in term_fees.fees.all():
                total = total + f.amount
            return total
        return total


class FeeSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source = 'student_class.name',read_only=True)
    class Meta:
        model = Fee
        fields = (
        'id','type','name','amount','class_name',
        )

class StudentClassFeesSerializer(serializers.ModelSerializer):
    term = TermSerializer(many=False,read_only=True)
    fees = FeeSerializer(many=True,read_only=True)
    class Meta:
        model = IndividualClassFees
        fields = (
        'id','term','fees',
        )

class StudentClassSerializer(serializers.ModelSerializer):
    class_fees = StudentClassFeesSerializer(many = True,read_only=True)
    total_students = serializers.SerializerMethodField()
    total_fees = serializers.SerializerMethodField()

    class Meta:
        model = StudentClass
        fields = (
            'id','name','class_fees','total_students','total_fees'
        )
    
    def create(self,validated_data):
        student_class = StudentClass.objects.create(**validated_data)           
        return student_class
    
    def get_total_students(self,obj):
        students = Student.objects.filter(id = obj.id).count()
        return students
    
    def get_total_fees(self,obj):
        total = 0
        qs_exists= IndividualClassFees.objects.filter(student_class=obj.id).exists()
        if(qs_exists):
            class_fees = IndividualClassFees.objects.get(student_class=obj.id)
            fees = class_fees.fees.all()
            for f in fees:
                total = total + f.amount
            return total
        return total


class SubjectUnitSerializer(serializers.ModelSerializer):
    # StringRelatedField may be used to represent the target of the relationship using its __str__ method.
    # This field is read only.
    student_classes = serializers.StringRelatedField(many = True,read_only=True)
    class Meta:
        model = SubjectUnit
        fields = (
            'id','name','code_name','name_short_form','student_classes',
        )
