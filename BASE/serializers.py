from rest_framework import serializers
from .models import SchoolType, Region, School, GradeSubject, Subject, Grade

class SchoolTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolType
        fields = '__all__'

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'
class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['libar']
class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['libar','libfr']
class GradeSubjectSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    grade = GradeSerializer(read_only=True)
    class Meta:
        model = GradeSubject
        fields = ['id','grade','subject']


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'