from rest_framework import serializers
from .models import Course
from BASE.serializers import GradeSubjectSerializer

class CourseSerializer(serializers.ModelSerializer):
    grade_subject = GradeSubjectSerializer(read_only=True)
    poster = serializers.SerializerMethodField()
    poster_pic = serializers.SerializerMethodField()
    course_contents = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = '__all__'
    def get_poster(self, obj):
        return obj.poster.first_name + ' ' + obj.poster.last_name

    def get_poster_pic(self, obj):
        return obj.poster.profile.picture.url
    def get_course_contents(self, obj):
        return [content.file.url for content in obj.contents.all()]
