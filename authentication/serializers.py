from rest_framework import serializers
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import GroupCategory, Userprofile
from mulumba.utils import get_content_type

# User objects have two many-to-many fields: groups and user_permissions.
# User objects can access their related objects in the same way as any other Django model:

class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = "__all__"

class PermissionSerializer(serializers.ModelSerializer):
    content_type_name = serializers.CharField(source="content_type.name") #Accessing in create/update => validated_data['content_type']['name']
    class Meta:
        model = Permission
        fields = ('id','name','codename','content_type','content_type_name')
    
    def create(self, validated_data):
        content_type = ContentType.objects.get(model = validated_data['content_type']['name'])
        perm_instance = Permission.objects.create(name=validated_data['name'],codename = validated_data['codename'],content_type = content_type)
        return perm_instance

class ContentTypePermissionSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()
    class Meta:
        model = ContentType
        fields = ('id','name','permissions',)
    
    def get_permissions(self,instance):
        permissions = Permission.objects.filter(content_type = instance.id)
        return PermissionSerializer(permissions,many=True).data

class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many= True,read_only =True)
    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'permissions', 
            )

class GroupCategorySerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many= True,read_only =True)
    class Meta:
        model = GroupCategory
        fields = (
            'id',
            'name',
            'groups', 
            )

class AddObjectPermissionsToGroupSerializer(serializers.ModelSerializer):
    app_label = serializers.CharField(write_only=True, required=True)
    model = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Group
        fields = ('app_label','model')
    
    def update(self, instance, validated_data):
        content_type = get_content_type(validated_data['app_label'], validated_data['model'])
        permissions = Permission.objects.filter(content_type = content_type)
        for p in permissions:
            instance.permissions.add(p)
        return instance

class RemoveObjectPermissionsFromGroupSerializer(serializers.ModelSerializer):
    app_label = serializers.CharField(write_only=True, required=True)
    model = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Group
        fields = ('app_label','model')
    
    def update(self, instance, validated_data):
        content_type = get_content_type(validated_data['app_label'], validated_data['model'])
        permissions = Permission.objects.filter(content_type = content_type)
        for p in permissions:
            instance.permissions.remove(p)
        return instance

class UserSerializer(serializers.ModelSerializer):
    #Suppose we want the key to be user_name instead of the orignal username of User model, *use source
    user_name = serializers.CharField(source = "username")
    user_groups = GroupSerializer(source='groups',many=True,read_only=True)
    my_permissions = PermissionSerializer(source='user_permissions',many = True,read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            'user_name',
            'email',
            'first_name',
            'last_name',
            'is_active',
            'user_groups',
            'my_permissions',
            )

class AddUserToGroupSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('group_name',)
    
    def update(self, instance, validated_data):
        group = Group.objects.get(name = validated_data["group_name"])        
        instance.groups.add(group)
        return instance

class RemoveUserFromGroupSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('group_name',)
    
    def update(self, instance, validated_data):
        group = Group.objects.get(name = validated_data["group_name"])        
        instance.groups.remove(group)
        return instance

# class UserprofileSerializer(serializers.ModelSerializer):
#     fullname = serializers.SerializerMethodField(read_only = True)

#     def get_fullname(self, obj):
#         # return "%s %s" (obj.firstname, obj.lastname)
#         return obj.firstname + " " + obj.lastname

#     #for returning a nested serializer
#     profileOwner = UserSerializer(source="user",many=False)
#     profileOwnerusername = serializers.CharField(source="user.username")

#     class Meta:
#         model = Userprofile
#         fileds = (
#             "username",
#             "profileOwner",
#             "profileOwnerusername",
#             "firstname",
#             "lastname",
#             "othername",
#             "fullname",
#         )

#Many To Many Field Relationships Between User And Group Models
#Getting all users belonging to a certain group
    #my_group.user_set.all()
#Adding a user to a certain group
    #my_group.user_set.add(u)
#Getting all groups a user belongs to
    #my_user.groups.all()
#Adding a user to a certain group
    #my_user.groups.add(g)

#Many To Many Field Relationships Between User And Permission Models
#Getting all users that have a certain user_permission
    #my_permission.user_set.all()
#Adding a user to a certain user_permission
    #my_permission.user_set.add(u)
#Getting all user_permissions a user has
    #my_user.user_permissions.all()
#Adding a user to a certain user_permission
    #my_user.user_permissions.add(p)

#Many To Many Field Relationships Between Group And Permission Models
#Getting all groups that have a certain user_permission
    #my_permission.group_set.all()
#Adding a user to a certain user_permission
    #my_permission.group_set.add(g)
#Getting all user_permissions a group has
    #my_group.permissions.all()
#Adding a group to a certain user_permission
    #my_group.permissions.add(p)
