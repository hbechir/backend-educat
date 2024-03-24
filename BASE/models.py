from django.db import models
from django.contrib.auth.models import User


class Region(models.Model):
    libar = models.CharField(max_length=255)
    def __str__(self):
        return self.libar

class SchoolType(models.Model):
    libar = models.CharField(max_length=255)

    def __str__(self):
        return self.libar

class School(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    school_type = models.ForeignKey(SchoolType, on_delete=models.CASCADE)
    codeetab=models.IntegerField()  
    libar = models.CharField(max_length=255)

    def __str__(self):
        return self.libar


class Grade(models.Model):
    libfr = models.CharField(max_length=255)
    libar = models.CharField(max_length=255)
    subjects = models.ManyToManyField('Subject', through='GradeSubject', related_name='grades_for_subject')
    SchoolType = models.ForeignKey(SchoolType, on_delete=models.CASCADE)
    def __str__(self):
        return self.libfr

class Subject(models.Model):
    libfr = models.CharField(max_length=255)
    libar = models.CharField(max_length=255)
    grades = models.ManyToManyField(Grade, through='GradeSubject', related_name='subjects_for_grade')
    def __str__(self):
        return self.libar + " | " + self.libfr



class GradeSubject(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    def __str__(self):
        return self.grade.libfr +" | "+self.subject.libfr