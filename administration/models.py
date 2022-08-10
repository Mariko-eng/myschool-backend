from django.db import models
from django.contrib.auth.models import User,Group
from django.core.files import File
from io import BytesIO
from PIL import Image
from mulumba.utils import random_string_generator
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

class Term(models.Model):
    CHOICES = [
        ('First Term','First Term'), 
        ('Second Term','Second Term'),
        ('Third Term','Third Term'),
    ]
    STATUS = [
        ('Pending','Pending'),
        ('Running','Running'),
        ('Completed','Completed'), 
    ]
    name = models.CharField(choices=CHOICES, max_length=200, blank=True,null=True)
    start_date = models.DateField(null=True,unique=True)
    end_date = models.DateField(null=True,unique=True)
    academic_year = models.IntegerField(null=True)
    is_approved = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS, max_length=200, default="Pending")
    created_by = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)

class StudentClass(models.Model):
    LEVEL = [
        ('Lower','Lower'), 
        ('Higher', 'Higher'),
    ]
    name = models.CharField(max_length=200,unique=True)
    level = models.CharField(choices=LEVEL,max_length=100,blank=True,null=True)

    def __str__(self) -> str:
        return self.name
    

class SubjectUnit(models.Model):
    name = models.CharField(max_length=200)
    name_short_form = models.CharField(max_length=200,null=True,blank=True)
    code_name = models.CharField(max_length=200,unique=True,null=True,blank=True)
    student_classes = models.ManyToManyField(StudentClass)

    def __str__(self) -> str:
        return self.name


class Staff(models.Model):
    user = models.ForeignKey(User,related_name = "staff_account",null = True,on_delete=models.SET_NULL)
    roles = models.ManyToManyField(Group,related_name = "staff_roles")
    username = models.CharField(max_length=200,null=True,blank=True,unique=True)
    staff_id = models.CharField(max_length=200,null=True,blank=True,unique=True)
    is_teacher = models.BooleanField(default=True)
    teacher_subjects = models.ManyToManyField(SubjectUnit)
    teacher_student_classes = models.ManyToManyField(StudentClass)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    given_name = models.CharField(max_length=200,null=True,blank=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=200,null=True,blank=True)
    phone_number = models.CharField(max_length=200,null=True,blank=True,unique=True)
    email = models.CharField(max_length=200,null=True,blank=True)
    nationality = models.CharField(max_length=200,null=True,blank=True)
    national_id = models.CharField(max_length=200,null=True,blank=True)
    religion = models.CharField(max_length=200,null=True,blank=True)
    profession = models.CharField(max_length=200)
    previous_work_place = models.CharField(max_length=200,null=True,blank=True)
    experience = models.CharField(max_length=200,null=True,blank=True)
    home_address_district = models.CharField(max_length=200,null=True,blank=True)
    home_address_village = models.CharField(max_length=200,null=True,blank=True)
    has_a_disability = models.BooleanField(default=False)
    disabilities = models.TextField(blank=True,null=True)
    hobbies_or_skills = models.TextField(blank=True,null=True)
    food_dislikes = models.TextField(blank=True,null=True)
    image = models.ImageField(upload_to='staff/images/',blank=True,null = True)
    thumbnail = models.ImageField(upload_to = 'staff/thumnails/', blank=True,null = True)
    
    def get_age(self):
        pass    
    
    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        else:
            return ''
    
    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(300,200)):
        img = Image.open(image)
        img.convert('RGB') # MAkes The Image Transparent
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, 'PNG', quality=85)
        # transparent image can’t be stored into jpg or jpeg format
        # Can only be stored in PNG format 
        thumbnail = File(thumb_io, name=image.name)
        return thumbnail

@receiver(pre_save, sender = Staff)
def unique_staff_id_generator(instance, *args,**kwargs):
    id = random_string_generator(size=7)
    id = "STF-" + id.upper()
    qs_exists = Staff.objects.filter(staff_id= id).exists()
    if(qs_exists):
        return unique_staff_id_generator(instance,*args,**kwargs)
    else:
        instance.staff_id = id

@receiver(pre_save, sender = Staff)
def unique_staff_username_generator(instance, *args,**kwargs):
    xId = random_string_generator(size=4)
    username = instance.first_name + xId.upper()
    qs_exists = Staff.objects.filter(username= username).exists()
    if(qs_exists):
        return unique_staff_username_generator(instance,*args,**kwargs)
    else:
        instance.username = username

class ParentsData(models.Model):
    father_first_name = models.CharField(max_length=200,null=True,blank=True)
    father_last_name = models.CharField(max_length=200,null=True,blank=True)
    father_phone_number = models.CharField(max_length=200,null=True,blank=True)
    father_email = models.CharField(max_length=200,null=True,blank=True)
    father_profession = models.CharField(max_length=200,null=True,blank=True)
    father_work_place = models.CharField(max_length=200,null=True,blank=True)
    father_nationality = models.CharField(max_length=200,null=True,blank=True)
    is_father_alive = models.BooleanField(default=True,null=True)
    mother_first_name = models.CharField(max_length=200,null=True,blank=True)
    mother_last_name = models.CharField(max_length=200,null=True,blank=True)
    mother_phone_number = models.CharField(max_length=200,null=True,blank=True)
    mother_email = models.CharField(max_length=200,null=True,blank=True)
    mother_profession = models.CharField(max_length=200,null=True,blank=True)
    mother_work_place = models.CharField(max_length=200,null=True,blank=True)
    mother_nationality = models.CharField(max_length=200,null=True,blank=True)
    is_mother_alive = models.BooleanField(default=True,null=True)
    guardain_first_name = models.CharField(max_length=200,null=True,blank=True)
    guardain_last_name = models.CharField(max_length=200,null=True,blank=True)
    guardain_phone_number = models.CharField(max_length=200,null=True,blank=True)
    guardian_email = models.CharField(max_length=200,null=True,blank=True)
    guardian_nationality = models.CharField(max_length=200,null=True,blank=True)
    guardian_work_place = models.CharField(max_length=200,null=True,blank=True)
    guardian_profession = models.CharField(max_length=200,null=True,blank=True)
    contact_nationalId_name = models.CharField(max_length=200,null=True,blank=True)
    contact_national_id = models.CharField(max_length=200,null=True,blank=True)
    contact_nationality_relation = models.CharField(max_length=200,null=True,blank=True)
    home_address_district = models.CharField(max_length=200,null=True,blank=True)
    home_address_village = models.CharField(max_length=200,null=True,blank=True)


class Student(models.Model):
    user = models.ForeignKey(User,related_name = "user_account",null = True,on_delete=models.SET_NULL)
    roles = models.ManyToManyField(Group,related_name = "student_roles")
    username = models.CharField(max_length=200,null=True,blank=True,unique=True)
    student_id = models.CharField(max_length=200,null=True,blank=True)
    student_class = models.ForeignKey(StudentClass,on_delete=models.SET_NULL,null=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    given_name = models.CharField(max_length=200,null=True,blank=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=200,null=True,blank=True)
    nationality = models.CharField(max_length=200,null=True,blank=True)
    religion = models.CharField(max_length=200,null=True,blank=True)
    is_baptised = models.BooleanField(null=True)
    parents_info = models.ForeignKey(ParentsData,related_name = "student",null = True,on_delete=models.SET_NULL)
    has_a_disability = models.BooleanField(default=False)
    disabilities = models.TextField(blank=True,null=True)
    hobbies_or_skills = models.TextField(blank=True,null=True)
    food_dislikes = models.TextField(blank=True,null=True)
    previous_school = models.CharField(max_length=200,null=True,blank=True)
    previous_school_class = models.CharField(max_length=200,null=True,blank=True)
    image = models.ImageField(upload_to='students/images/',blank=True,null = True) # wiil be uploaded to MEDIA_ROOT/myFiles
    thumbnail = models.ImageField(upload_to = 'students/thumnails/', blank=True,null = True)

    def get_age(self):
        pass

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        else:
            return ''
    
    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(300,200)):
        img = Image.open(image)
        img.convert('RGB') # MAkes The Image Transparent
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'PNG', quality=85)
        # transparent image can’t be stored into jpg or jpeg format
        # Can only be stored in PNG format 

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail    

@receiver(pre_save, sender = Student)
def unique_student_id_generator(instance, *args, **kwargs):
    id = random_string_generator(size=7)
    id = "P-" + id.upper()
    qs_exists = Student.objects.filter(student_id = id).exists()
    if(qs_exists):
        return unique_student_id_generator(instance, *args, **kwargs)
    else:
        instance.student_id = id

@receiver(pre_save, sender = Student)
def unique_student_username_generator(instance, *args,**kwargs):
    xId = random_string_generator(size=4)
    username = instance.first_name + xId.upper()
    qs_exists = Student.objects.filter(username= username).exists()
    if(qs_exists):
        return unique_student_username_generator(instance,*args,**kwargs)
    else:
        instance.username = username
