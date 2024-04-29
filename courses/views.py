from django.shortcuts import render
from .models import Course, CourseContent
from .serializers import CourseSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.core.files.storage import default_storage
from BASE.models import GradeSubject



# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCoursesByFilters(request):
    user=request.user
    # check for privided filters (grade_subject, title), if not provided return all courses with the same grade as the user
    grade_subject = request.GET.get('grade_subject')
    title = request.GET.get('title')
    print(grade_subject)
    print(title)
    if grade_subject=='' and title=='':
        # get grade_subjects of the user's grade
        grade_subjects = user.profile.grade.gradesubject_set.all()
        # get courses of the grade_subjects
        courses = Course.objects.filter(grade_subject__in=grade_subjects)
    elif grade_subject=='':
        # get grade_subjects of the user's grade
        grade_subjects = user.profile.grade.gradesubject_set.all()
        # get courses of the grade_subjects
        courses = Course.objects.filter(grade_subject__in=grade_subjects, title__icontains=title)
    elif title=='':
        # get courses of the grade_subjects
        courses = Course.objects.filter(grade_subject=grade_subject)
    else:
        # get courses of the grade_subjects
        courses = Course.objects.filter(grade_subject=grade_subject, title__icontains=title)
    serializer = CourseSerializer(courses, many=True)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addCourse(request):
    user = request.user
    print(request.data)
    grade_subject_id = request.data.get('grade_subject')
    title = request.data.get('title')

    # Get the GradeSubject instance
    try:
        grade_subject = GradeSubject.objects.get(id=grade_subject_id)
    except GradeSubject.DoesNotExist:
        return Response({"error": "GradeSubject not found"}, status=404)


    # get the user's school
    school = user.profile.school
    # Create a new Course instance and save it to the database
    course = Course(title=title, grade_subject=grade_subject, poster=user, school=school)
    course.save()

    for key in request.FILES.keys():
        if key.startswith('files'):
            file = request.FILES[key]
            course_content = CourseContent(course=course, file=file)
            course_content.save()

    # Return a response
    return Response({"message": "Course created successfully"}, status=201)