from rest_framework import serializers
from .models import Question, Answer, Upvote, QuestionImage

from rest_framework.fields import BooleanField
from BASE.serializers import GradeSubjectSerializer
from BASE.models import GradeSubject

class QuestionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionImage
        fields = ['image']

class QuestionSerializer(serializers.ModelSerializer):
    images = QuestionImageSerializer(many=True, read_only=True)
    author_grade = serializers.SerializerMethodField()
    has_unfetched_answers = serializers.SerializerMethodField()
    grade_subject = serializers.PrimaryKeyRelatedField(queryset=GradeSubject.objects.all())

    class Meta:
        model = Question
        fields = ['id','author','grade_subject','has_unfetched_answers', 'author_grade', 'question_text', 'question_detail', 'score', 'date_pub', 'audience', 'solved', 'upvotes', 'images']

    def get_author_grade(self, obj):
        return obj.author.profile.grade.libfr

    def get_has_unfetched_answers(self, obj):
        return obj.has_unfetched_answers()

class QuestionSerializer(serializers.ModelSerializer):
    images = QuestionImageSerializer(many=True, read_only=True)
    author_grade = serializers.SerializerMethodField()
    has_unfetched_answers = serializers.SerializerMethodField()
    grade_subject_dict = serializers.SerializerMethodField()
    user_upvoted = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id','author','grade_subject_dict','grade_subject','has_unfetched_answers', 'author_grade', 'question_text', 'question_detail', 'score', 'date_pub', 'audience', 'solved','user_upvoted', 'upvotes', 'images']

    def get_author_grade(self, obj):
        return obj.author.profile.grade.libfr

    def get_has_unfetched_answers(self, obj):
        return obj.has_unfetched_answers()

    def get_grade_subject_dict(self, obj):
        return GradeSubjectSerializer(obj.grade_subject).data
    def get_user_upvoted(self, obj):
        request = self.context.get('request')
        if request:
            user = request.user
            print(user)
            if user.is_authenticated:
                return Upvote.objects.filter(question=obj, user=user).exists()
        return False

class AnswerSerializer(serializers.ModelSerializer):
    author_first_name = serializers.SerializerMethodField()
    author_last_name = serializers.SerializerMethodField()
    class Meta:
        model = Answer
        fields = ['id','question','accepted', 'author', 'author_first_name', 'author_last_name', 'answer_text', 'score', 'date_pub', 'upvotes']

    def get_author_first_name(self, obj):
        return obj.author.first_name

    def get_author_last_name(self, obj):
        return obj.author.last_name
