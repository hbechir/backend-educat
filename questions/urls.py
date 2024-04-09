from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.GetRecommendations),
    path('personal/', views.GetPersonalQuestions),
    path('shuffle/', views.ShuffleRecommendations),
    path('ask/', views.QuestionCreate),
    path('question-answers/', views.getAnswers),
    path('upvote/', views.upvote),
    path('answer/', views.answer),
    path('accept-answer/', views.accept),
    
]
