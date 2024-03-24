from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random

from BASE.models import School, Grade

# Create your models here.
class Profile(models.Model):
    role_choices = (
        ('student', 'student'),
        ('provider', 'provider'),
        ('admin', 'admin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=role_choices, default='student')
    verified = models.BooleanField(default=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, null=True, blank=True)
    credit = models.FloatField(default=0,null=False, blank=False)
    finished = models.BooleanField(default=False)
    lat = models.FloatField(default=None, null=True, blank=True)
    lng = models.FloatField(default=None, null=True, blank=True)
    picture = models.ImageField(upload_to='profile_pics', default='profile_pics/default.png', null=True, blank=True)

    
    def __str__(self):
        return self.user.username




class VerificationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_code(self):
        # Delete the old code if it exists
        VerificationCode.objects.filter(user=self.user).delete()
        print("generate code")

        # Generate a new random 6-digit code
        self.code = str(random.randint(10000,99999 ))
        self.save()

    def is_valid(self, user):
        # Check if the code is less than 10 minutes old and the user is the same
        return (timezone.now() - self.created_at).total_seconds() < 600 and self.user == user