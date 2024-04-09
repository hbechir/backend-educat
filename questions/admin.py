from django.contrib import admin
from .models import Question, Answer, Upvote, QuestionImage, UserRecommendations
# Register your models here.
admin.site.register(QuestionImage)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Upvote)
admin.site.register(UserRecommendations)
