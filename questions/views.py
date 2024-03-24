from django.shortcuts import render
from .models import Question, Answer , Upvote , QuestionImage, UserRecommendations

from .serializers import QuestionSerializer, AnswerSerializer 
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from . import utils
from django.utils import timezone

from datetime import timedelta




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetPersonalQuestions(request):
    questions = Question.objects.filter(author=request.user).order_by('-date_pub')
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetRecommendations(request):
    try:
        user_recommendations = UserRecommendations.objects.get(user=request.user)
        serializer = QuestionSerializer(user_recommendations.questions.all(), many=True,context={'request': request})
        time_to_next_shuffle = max(0, (user_recommendations.last_updated + timedelta(minutes=0.5) - timezone.now()).total_seconds())
        return Response({'questions': serializer.data, 'time_to_next_shuffle': time_to_next_shuffle})
    except UserRecommendations.DoesNotExist:
        utils.generate_recommendations(request.user)
        user_recommendations = UserRecommendations.objects.get(user=request.user)
        serializer = QuestionSerializer(user_recommendations.questions.all(), many=True)
        time_to_next_shuffle = max(0, (user_recommendations.last_updated + timedelta(minutes=0.5) - timezone.now()).total_seconds())
        return Response({'questions': serializer.data, 'time_to_next_shuffle': time_to_next_shuffle})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ShuffleRecommendations(request):
    try:
        user_recommendations = UserRecommendations.objects.get(user=request.user)
        time_passed = timezone.now() - user_recommendations.last_updated
        print(timezone.now())
        print(user_recommendations.last_updated)
        print(time_passed)
        if time_passed > timedelta(minutes=0.5):
            
            utils.generate_recommendations(request.user)
            user_recommendations.last_updated = timezone.now()
            user_recommendations.save()
        return Response({'message': 'Recommendations shuffled'})
    except UserRecommendations.DoesNotExist:
        utils.generate_recommendations(request.user)
        return Response({'message': 'Recommendations shuffled'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def QuestionCreate(request):
    data = request.data.copy()  # Make a mutable copy of the data

    data['author'] = request.user.id  # Add the user id to the data
    # Convert 'grade_subject' from list of strings to integer
    data['grade_subject'] = int(data['grade_subject'][0])
    print(data)
    serializer = QuestionSerializer(data=data)
    
    if serializer.is_valid():
        question = serializer.save()
        # Save the images if they're in the request
        for key in request.FILES:
            if 'image' in key:
                image_file = request.FILES[key]
                QuestionImage.objects.create(question=question, image=image_file)
        return Response(serializer.data)
    print(serializer.errors)    
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAnswers(request):
    id = request.GET.get('question')  # Get the ID from the query parameters
    try:
        question = Question.objects.get(id=id)
        answers = question.answer_set.all()
        # check if the current user is the owner of the question
        if question.author == request.user:
            answers.update(fetched=True)

        answersSerializer = AnswerSerializer(answers, many=True)

        user_answered = question.answer_set.filter(author=request.user).exists()

        return Response({
            'answers': answersSerializer.data,
            'user_answered': user_answered
        })
    except Exception as e:
        return Response({'message': 'Question not found'}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upvote(request):

    try:
        question = Question.objects.get(id=request.data['id'])
        user = request.user
    except:
        return Response({'message':'Question not found'}, status=400)
    try:
        upvote = Upvote.objects.get(question=question, user=user)
        print(upvote)
        return Response({'message':'Question already upvoted'}, status=400)
    except:
        question.upvotes += 1
        question=utils.question_upvote_score(question)
        cost=utils.user_question_upvote_credit(user,question)
        upvote = Upvote(user=user, question=question, cost=cost)
        upvote.save()
        question.save()
        return Response({'message':'Upvoted'})






# answers ---------------------------------------------------------------------------------------------

@api_view(['POST'])
@permission_classes([IsAuthenticated])
#a user is as able to send only 1 answer per question
def answer(request):
    data = request.data.copy()
    data['author'] = request.user.id
    #check if the author is answering his own question
    question = Question.objects.get(id=data['question'])
    if question.author == request.user:
        return Response({'message':'You cannot answer your own question'}, status=400)
    try:
        answer = Answer.objects.get(question=data['question'], author=data['author'])
        return Response({'message':'You have already answered this question'}, status=400)
    except:
        serializer = AnswerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            utils.question_answer_score(data['question'])
            utils.user_answer_credit(request.user)
            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status=400)





@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept(request):
    answer = Answer.objects.get(id=request.data['answer'])
    question = Question.objects.get(id=answer.question.id)
    if question.author == request.user:
        answer.accepted = True
        question.solved = True

        # Reward upvoters, answerers, and the accepted answer author
        utils.accept_answer_credit(answer.author)
        utils.reward_upvoters(question)
        utils.reward_answerers(question)
        utils.reward_accepted_answer_author(question,answer)
        answer.save()
        question.save()
        return Response({'message':'Answer accepted'})

    return Response({'message':'You are not the author of this question'})