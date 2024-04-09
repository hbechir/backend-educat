from django.shortcuts import render
from .models import School,Region,SchoolType,GradeSubject,Grade
from .serializers import SchoolSerializer,RegionSerializer,SchoolTypeSerializer,GradeSubjectSerializer,GradeSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSchoolsByRegionAndType(request):
    region = request.GET.get('region')
    school_type = request.GET.get('school_type')
    schools = School.objects.filter(region=region, school_type=school_type)
    serializer = SchoolSerializer(schools, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllSchoolTypes(request):
    school_types = SchoolType.objects.all()
    serializer = SchoolTypeSerializer(school_types, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getGradesBySchoolType(request):
    school_type = request.GET.get('school_type')
    grades = Grade.objects.filter(SchoolType=school_type)
    serializer = GradeSerializer(grades, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllRegions(request):
    regions = Region.objects.all()
    serializer = RegionSerializer(regions, many=True)
    return Response(serializer.data)



# this is for gettting grade subjects accoring to the users grade in the profile 


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getGradeSubjects(request):
    user=request.user
    grade = user.profile.grade
    grade_subjects = GradeSubject.objects.filter(grade=grade)
    serializer = GradeSubjectSerializer(grade_subjects, many=True)
    return Response(serializer.data)
    