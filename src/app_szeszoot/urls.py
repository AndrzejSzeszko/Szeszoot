#!/usr/bin/python3.7
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('/', views.HomeView.as_view(), name='home'),
    path('sign_up/', views.SignInView.as_view(), name='sign-up'),
    path('login/', auth_views.LoginView.as_view(template_name='app_szeszoot/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='app_szeszoot/logout.html'), name='logout'),
    path('quiz_add/', views.AddQuizView.as_view(), name='quiz-add'),
    path('question_create/<str:quiz_title>/', views.QuestionCreateView.as_view(), name='question-create'),
    path('set_up_game/quiz_list/', views.QuizListView.as_view(), name='quiz-list'),
    path('game_create/<int:quiz_pk>/', views.GameCreateView.as_view(), name='game-create'),
    path('game_master_panel/<int:game_pk>/', views.GameMasterPanelView.as_view(), name='game-master-panel'),
    path('player_create/', views.PlayerCreateView.as_view(), name='player-create'),
    path('player_panel/<int:pk>/', views.PlayerPanelView.as_view(), name='player-panel'),
]
