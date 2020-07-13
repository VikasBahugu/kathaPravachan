from django.contrib import admin
from home.models import ContactUser, Profile, SigningUser, Newsletter, AnswerQuestions


admin.site.register((ContactUser, Profile, SigningUser, Newsletter, AnswerQuestions))
