from django.contrib import admin
from home.models import ContactUser, Profile, SigningUser, Newsletter, AnswerQuestion, Twelve_rashi, Videoblog_video


admin.site.register((ContactUser, Profile, SigningUser, Newsletter, AnswerQuestion, Twelve_rashi, Videoblog_video))
