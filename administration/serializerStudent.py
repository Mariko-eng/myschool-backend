from .models import ParentsData,Student
from .models import StudentClass
from authentication.serializers import GroupSerializer
from django.contrib.auth.models import User,Group
from .serializersCommon import StudentClassSerializer
from rest_framework import serializers

class  ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentsData
        fields = "__all__"

class  StudentSummarySerializer(serializers.ModelSerializer):
    roles = GroupSerializer(many = True,read_only =True)
    class Meta:
        model = Student
        fields = (
            'id','user',
            'roles',
            'student_id','student_class',
            'first_name', 'last_name',
            'given_name','gender',
        )

class  StudentSerializer(serializers.ModelSerializer):
    roles = GroupSerializer(many = True,read_only =True)
    student_class = StudentClassSerializer(many = False,read_only=True)
    parents_info = ParentSerializer()
    key = serializers.CharField(source = 'student_id')
    class Meta:
        model = Student
        fields = (
            'id','key','user','student_id','student_class',
            'roles','first_name', 'last_name','given_name',
            'date_of_birth','gender',
            'nationality','religion','is_baptised',
            'has_a_disability',
            'disabilities','hobbies_or_skills',
            'food_dislikes',
            'previous_school',
            'previous_school_class','parents_info',
        )

class ChosenClassesSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()

class  StudentRegistrationSerializer(serializers.ModelSerializer):
    roles = GroupSerializer(many = True,read_only =True)
    xklass = ChosenClassesSerializer(many=False,write_only=True)
    parents_info = ParentSerializer(many=False)

    class Meta:
        model = Student
        fields = (
            'user','student_id','student_class',
            'roles','first_name', 'last_name','given_name',
            'date_of_birth','gender','nationality',
            'religion','is_baptised','parents_info',
            'has_a_disability',
            'disabilities','hobbies_or_skills',
            'food_dislikes',
            'previous_school','previous_school_class',
            'xklass',
        )

    def create(self,validated_data):
        qs_exists = Group.objects.filter(name = "Student").exists()
        if(qs_exists):
            role = Group.objects.get(name = "Student")
        else:
            role = Group.objects.create(name="Student")
            
        xclass = validated_data.pop("xklass")            
        parents_data = validated_data.pop("parents_info")

        parent = ParentsData.objects.create(**parents_data)
        xKlass = StudentClass.objects.get(id = xclass['id'])

        student = Student.objects.create(student_class = xKlass,parents_info = parent, **validated_data)
        user_accoount = User.objects.create(username = student.username,password = student.student_id)
        student.user = user_accoount
        student.save()
        student.roles.add(role)
        return student
