#!/usr/bin/python3.7
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('sign_up/', views.SignInView.as_view(), name='sign-up'),
    path('login/', auth_views.LoginView.as_view(template_name='app_szeszoot/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='app_szeszoot/logout.html'), name='logout'),
    path('quiz_add/', views.AddQuizView.as_view(), name='quiz-add'),
    path('question_create/<str:quiz_title>/', views.QuestionCreateView.as_view(), name='question-create'),
    path('set_up_game/quiz_list/', views.QuizListView.as_view(), name='quiz_list'),
    path('quiz_panel/<int:pk>/', views.QuizPanelView.as_view(), name='quiz-panel'),
    path('player_create/', views.PlayerCreateView.as_view(), name='player-create'),
    path('game/<int:pk>/', views.GameView.as_view(), name='game'),
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
]
