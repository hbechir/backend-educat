from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User
from BASE.models import School

from rest_framework import serializers
from BASE.serializers import SchoolSerializer



class ProfileSerializer(serializers.ModelSerializer):
    school = SchoolSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = ['user','role', 'verified', 'school', 'grade', 'credit', 'finished', 'lat', 'lng', 'picture']
    
