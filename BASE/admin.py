from django.contrib import admin


# Register your models here.

#register your models here.
from .models import Region, SchoolType, School, Grade, Subject, GradeSubject

admin.site.register(Region)
admin.site.register(SchoolType)
admin.site.register(School)
admin.site.register(Grade)
admin.site.register(Subject)
admin.site.register(GradeSubject)

