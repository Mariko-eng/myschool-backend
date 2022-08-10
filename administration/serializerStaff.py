from .models import Staff,SubjectUnit,StudentClass
from .serializersCommon import SubjectUnitSerializer,StudentClassSerializer
from authentication.serializers import GroupSerializer
from django.contrib.auth.models import User,Group
from rest_framework import serializers

class StaffSerializer(serializers.ModelSerializer):
    roles = GroupSerializer(many = True)
    # teacher_subjects = SubjectUnitSerializer(many = True)
    # teacher_student_classes = StudentClassSerializer(many = True)

    class Meta:
        model = Staff
        fields = (
            'id','user','roles','staff_id',
            # 'teacher_subjects','teacher_student_classes',
            'first_name', 'last_name','given_name',
            'date_of_birth', 'gender','phone_number','email',
            'is_teacher',
            'profession','nationality','national_id','religion',
            'previous_work_place','experience','has_a_disability',
            'disabilities','hobbies_or_skills',
            'food_dislikes',
           )

class ChosenSubjectsSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()

class ChosenClassesSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()

class TeachingStaffSerializer(serializers.ModelSerializer):
    roles = GroupSerializer(many = True,read_only =True)
    teacher_subjects = SubjectUnitSerializer(many = True,read_only =True)
    teacher_student_classes = StudentClassSerializer(many = True,read_only =True)
    subjects = ChosenSubjectsSerializer(many = True,write_only =True)
    classes = ChosenClassesSerializer(many = True,write_only =True)
    key = serializers.CharField(source = 'staff_id',read_only =True)

    class Meta:
        model = Staff
        fields = (
            'user','key','roles','staff_id',
            'first_name', 'last_name','given_name',
            'date_of_birth', 'gender','phone_number','email',
            'profession','nationality',
            'is_teacher',
            'national_id', 'religion','previous_work_place',
            'experience','has_a_disability',
            'teacher_subjects','teacher_student_classes',
            'disabilities','hobbies_or_skills',
            'food_dislikes',
            'subjects','classes',
        )
    
    def create(self,validated_data):
        qs_exists = Group.objects.filter(name = "Teacher").exists()
        if(qs_exists):
            role = Group.objects.get(name = "Teacher")
        else:
            role = Group.objects.create(name="Teacher")

        subjects = validated_data.pop("subjects")            
        classes = validated_data.pop("classes")

        staff = Staff.objects.create(**validated_data)

        for s in subjects:
            xsubject = SubjectUnit.objects.get(id = s['id'])
            staff.teacher_subjects.add(xsubject)

        for c in classes:
            xclass = StudentClass.objects.get(id = c['id'])
            staff.teacher_student_classes.add(xclass)

        staff.roles.add(role)
        user_accoount = User.objects.create(username = staff.username,password = staff.staff_id)
        staff.user = user_accoount
        staff.save()
        return staff

class ChosenRolesSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()

class ChosenOtherRolesSerializer(serializers.Serializer):
    name = serializers.CharField()

class NonTeachingStaffSerializer(serializers.ModelSerializer):
    roles = GroupSerializer(many = True,read_only =True)
    xroles = ChosenRolesSerializer(many = True,write_only =True)
    key = serializers.CharField(source = 'staff_id',read_only =True)

    class Meta:
        model = Staff
        fields = (
            'id','key','user','staff_id',
            'roles', 'xroles',
            'first_name', 'last_name','given_name',
            'date_of_birth', 'gender','phone_number','email',
            'profession','nationality','is_teacher',
            'national_id', 'religion','previous_work_place',
            'experience','has_a_disability',
            'disabilities','hobbies_or_skills',
            'food_dislikes',
            )
    
    def create(self,validated_data):
        roles = validated_data.pop("xroles")
        staff = Staff.objects.create(**validated_data)
        
        for s in roles:
            qs_exists = Group.objects.filter(name = s['name']).exists()
            if(qs_exists):
                role = Group.objects.get(name = s['name'])
                staff.roles.add(role)
            else:
                role = Group.objects.create(name=  s['name'])
                staff.roles.add(role)

        user_accoount = User.objects.create(username = staff.username,password = staff.staff_id)
        staff.user = user_accoount
        staff.save()
        return staff
