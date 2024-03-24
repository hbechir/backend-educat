from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from BASE.models import Subject

# Create your models here.



class Question(models.Model):
    AUDIENCE_CHOICES = [
        ('public', 'Public'),
        ('school', 'School'),
        ('class', 'Class'),
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    question_detail = models.TextField(max_length=1000)
    score = models.IntegerField(default=0)
    date_pub = models.DateTimeField('date published', default=timezone.now)
    audience = models.CharField(
        max_length=6,
        choices=AUDIENCE_CHOICES,
        default='public',
    )    
    solved = models.BooleanField(default=False)
    upvotes = models.IntegerField(default=0)
    grade_subject = models.ForeignKey('BASE.GradeSubject', on_delete=models.CASCADE, related_name='questions')
    def has_unfetched_answers(self):
        return self.answer_set.filter(fetched=False).exists()

        
        

    def __str__(self):
        return self.question_text

class QuestionImage(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='questions/images/', blank=True)


class UserRecommendations(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question)
    last_updated = models.DateTimeField(auto_now=True)

    
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)
    score = models.IntegerField(default=0)
    date_pub = models.DateTimeField('date published', default=timezone.now)
    accepted = models.BooleanField(default=False)
    upvotes = models.IntegerField(default=0)
    image = models.ImageField(upload_to='answers/images/', blank=True)
    fetched = models.BooleanField(default=False)
    def __str__(self):
        return self.answer_text
    


class Upvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, null=True, default=None)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, blank=True, null=True)
    date_pub = models.DateTimeField('date published', default=timezone.now)
    cost = models.FloatField(default=0)
    def __str__(self):
        return self.user.username + " " + str(self.question) + " " + str(self.answer)   

