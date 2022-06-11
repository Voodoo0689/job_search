from rest_framework import serializers
from mainapp.models import *


class UsersModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        exclude = (
            "hash_password",
            "email",
        )


class UserProfileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserJobHistoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserJobHistory
        fields = '__all__'


class UserEduModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEdu
        fields = '__all__'


class ArticlesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = '__all__'


class CityModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class RolesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'


class CompanyProfileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = '__all__'


class ResumesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


class CategoriesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


class VacancyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'