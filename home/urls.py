from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('singlepost', views.singlepost, name='singlepost'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('videoblog', views.videoblog, name='videoblog'),
    path('newsletter', views.newsletter, name='newsletter'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name="logout"),


    path('sharedkundali', views.shared_kundali, name='sharedkundali'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('answer_questions', views.answer_questions, name='answer_questions'),

    # path('single-post/<str:title>', views.singlePost, name='single-post'),
    # For posting a comment
    # path('postComment', views.postComment, name='postComment'),

    # path('single_post/<str:title>', views.singlePost, name='single_posts'),

    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='home/1_password_reset.html'),
         name="reset_password"),

    path('reset-password/sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='home/2_password_reset_sent.html'),
         name="password_reset_done"),

    path('reset-password/sent/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='home/3_password_reset_confirm.html'),
         name="password_reset_confirm"),

    path('reset-password/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='home/4_password_reset_complete.html'),
         name="password_reset_complete"),

    path('signup', views.signup, name='signup'),

    path('profile', views.profile, name='profile'),
    path('members', views.members, name='members'),

]
