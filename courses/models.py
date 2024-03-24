from django.db import models
from django.contrib.auth.models import User
from BASE.models import Subject, School, GradeSubject

# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=255)
    grade_subject = models.ForeignKey(GradeSubject, on_delete=models.CASCADE, related_name='contents')
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    credits = models.TextField(default="")

class CourseContent(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='contents')
    file = models.FileField(upload_to='course_contents/')
    