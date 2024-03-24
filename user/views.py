from django.shortcuts import render




# Create your views here.
from django.shortcuts import render
from .models import Profile
from .serializers import  ProfileSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.contrib.auth.models import User
from .models import Profile, VerificationCode
from BASE.models import School, Grade
from . import utils
from django.utils import timezone
from datetime import timedelta





#import to convert dict into json to return
import json


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def FinishProfile(request):
    user = request.user
    data = request.data
    print(data)

    # Get the school ID from the data
    school_id = data.get('school_id')
    if not school_id:
        return Response({'message': 'School ID is required'}, status=400)

    # Get the school with the provided ID
    try:
        school = School.objects.get(id=school_id)
    except School.DoesNotExist:
        return Response({'message': 'School not found'}, status=404)

    # Get the user's profile
    profile = Profile.objects.get(user=user)

    # Update the profile
    profile.school = school

    # get the grade from the data
    grade_id = data.get('grade_id')
    if not grade_id:
        return Response({'message': 'Grade ID is required'}, status=400)
    
    # Get the grade with the provided ID
    try:
        grade = Grade.objects.get(id=grade_id)
    except Grade.DoesNotExist:
        return Response({'message': 'Grade not found'}, status=404)

    # Update the profile
    profile.grade = grade

    profile.finished = True 
    profile.save()

    return Response({'message': 'Profile updated successfully'}, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def checkProfile(request):
    serializer = ProfileSerializer(request.user.profile)
    return Response(serializer.data)





@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password1 = request.data.get('password1')
    password2 = request.data.get('password2')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    picture = request.data.get('picture')

    # Check if all the data is provided
    fields = {'username': username, 'password1': password1, 'password2': password2, 'first_name': first_name, 'last_name': last_name}
    for field, value in fields.items():
        if not value:
            return Response({"message": field+' field is required'}, status=400)
    # Check if the username already exists
    try:
        user = User.objects.get(username=username)
        try :   
            verif=user.profile.verified # Check if the user is already verified
            return Response({'message': 'An account is already created with this phone number'}, status=400)
        except:
            user.delete()
    except User.DoesNotExist:
        pass

    # Check if the passwords match
    if password1 != password2:
        return Response({'message': 'Passwords do not match'}, status=400)

    # Check if the username is a valid phone number using Twilio
    if not utils.verify_phone_number(username):
        return Response({'message': 'Invalid phone number'}, status=400)

    #check picture adn create a user with all these info
    user = User.objects.create_user(username=username, password=password1, first_name=first_name, last_name=last_name)
    
    
    


    # Create the profile with the picture using the serializer
    profile_data = {'user': user.id, 'picture': picture}
    profile_serializer = ProfileSerializer(data=profile_data)
    if profile_serializer.is_valid():
        profile_serializer.save()
    else:
        print(profile_data)
        print(profile_serializer.errors)
        user.delete()
        return Response({"message":"there was an error"}, status=400)
    

    return Response({"message": "User created successfully,please proccede to login"})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_code(request):
    user = request.user

    # Delete the old verification code if it was created more than 1 minute ago or if it doesn't exist
    try:
        old_verification_code = VerificationCode.objects.get(user=user)
        time_since_code_sent = timezone.now() - old_verification_code.created_at
        if time_since_code_sent > timedelta(minutes=1):
            old_verification_code.delete()
        else:
            time_left = timedelta(minutes=1) - time_since_code_sent
            return Response({'message': f'Verification code already sent, please wait for {time_left.seconds} seconds.'})
    except VerificationCode.DoesNotExist:
        pass

    # Generate and send the new verification code
    verification_code = VerificationCode.objects.create(user=user)
    print(verification_code)
    verification_code.generate_code()
    utils.send_verification_code(user.username, verification_code.code, user.first_name)
    masked_username = '*****' + user.username[9:]
    return Response({'message': 'Verification code sent to'+masked_username+' successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify(request):
    user = request.user
    code = request.data.get('code')

    # Check if the code is valid
    try:
        verification_code = VerificationCode.objects.get(user=user)
    except VerificationCode.DoesNotExist:
        print('Verification code not sent')
        return Response({'message': 'Verification code not sent'}, status=400)

    if not verification_code.is_valid(user) or verification_code.code != code:
        print('Invalid verification code or expired')
        return Response({'message': 'Invalid verification code or expired'}, status=400)

    # Verify the user
    user.profile.verified = True
    user.profile.save()
    #delete the code
    verification_code.delete()

    
    return Response({'message': 'User verified successfully'})