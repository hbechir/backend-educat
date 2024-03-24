
from .models import Question, Answer
from django.utils import timezone
from django.contrib.auth.models import User
import random
from .models import Question, Answer , Upvote, UserRecommendations


def generate_recommendations(user):
    # Get all questions not authored by the user
    questions = Question.objects.exclude(author=user)

    # Randomly select 6 questions for each audience
    public_questions = [q for q in questions if q.audience == 'public']
    school_questions = [q for q in questions if q.audience == 'school' and q.author.profile.school == user.profile.school]

    recommended_public_questions = random.sample(public_questions, min(6, len(public_questions)))
    recommended_school_questions = random.sample(school_questions, min(6, len(school_questions)))       

    # Combine the lists of recommended questions
    recommended_questions = recommended_public_questions + recommended_school_questions

    # Update the user's recommendations
    try:
        user_recommendations = UserRecommendations.objects.get(user=user)
    except UserRecommendations.DoesNotExist:
        user_recommendations = UserRecommendations.objects.create(user=user)

    user_recommendations.questions.set(recommended_questions)



def question_upvote_score(question):
    #question score should be calculated as follows:
    #number of upvotes if excedes 5 then add 10 to the score
    #number of upvotes if excedes 10 then add 20 to the score
    #number of upvotes if excedes 30 then add 50 to the score
    if question.upvotes <=5:
        question.score += 2
    if question.upvotes >= 5:
        question.score += 10
    if question.upvotes >= 10:
        question.score += 20
    if question.upvotes >= 30:
        question.score += 50
    return question



def question_answer_score(question):
    #number of answers if the question has no accepted answer if excedes 5 then add 10 to the score
    #if the question has an accepted subsract 20 from the score
    question = Question.objects.get(id=question)
    answers = Answer.objects.filter(question=question)
    if len(answers) <= 5 and question.solved == False:
        question.score += 2
    if len(answers) >= 5 and question.solved == False:
        question.score += 10
    if len(answers) >= 10 and question.solved == False:
        question.score += 20
    if len(answers) >= 15 and question.solved == False:
        question.score += 20
    question.save()






# users credit -------------------------------------------------------------------------


def user_answer_credit(user):
    #add credit slightly less when the user is spamming answering questions(answered more than 5 questions in the last 10 minutes)
    #get the number of answers of the user in the last 10  minutes
    answers = Answer.objects.filter(author=user,date_pub__gte=timezone.now()-timezone.timedelta(minutes=10))
    profile= user.profile
    if len(answers) <= 3:
        profile.credit += 5
    elif len(answers) <= 5:
        profile.credit += 2
    elif len(answers) >= 5:
        profile.credit += 1
    elif len(answers) >= 10:
        profile.credit += 0.5
    profile.save()
    

def user_question_upvote_credit(user,question):
    #add credit slightly less when the user is spamming answering questions(answered more than 5 questions in the last 10 minutes)
    #get the number of upvotes of the user in the last 5 minutes
    profile= user.profile
    upvotes = Upvote.objects.filter(user=user,date_pub__gte=timezone.now()-timezone.timedelta(minutes=5))
    cost=0
    if len(upvotes) <= 3 :
        profile.credit -= 5
        cost=5
    elif len(upvotes) <= 8:
        profile.credit -= 2
        cost=2
    elif len(upvotes) >= 8:

        profile.credit -= 1
        cost=1
    profile.save()
    return cost
    
def accept_answer_credit(user):
    profile= user.profile
    profile.credit += 0.5
    profile.save()





# rewards --------------------------------------------------------------------------------------------

def reward_upvoters(question):
    upvotes = Upvote.objects.filter(question=question)
    for upvote in upvotes:
        upvote.user.profile.credit += 2 * upvote.cost
        upvote.user.profile.save()

def reward_answerers(question):
    answers = Answer.objects.filter(question=question)
    for answer in answers:
        answer.author.profile.credit += 0.1 * question.score
        answer.author.profile.save()

def reward_accepted_answer_author(question,answer):
    answer.author.profile.credit += 0.5 * question.score
    answer.author.profile.save()