#!/usr/bin/python3.7
from django import forms
from betterforms.multiform import MultiModelForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
)
from .models import (
    Quiz,
    Question,
    Answer,
    Player,
)

class SignInForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model  = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']


class UpdateCustomUserForm(UserChangeForm):
    class Meta:
        model  = get_user_model()
        fields = '__all__'


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = '__all__'


class QuestionForm(forms.ModelForm):
    class Meta:
        model   = Question
        exclude = ['quiz']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_content']


class QuestionAnswerForm(MultiModelForm):
    form_classes = {
        'question': QuestionForm,
        'answer1': AnswerForm,
        'answer2': AnswerForm,
        'answer3': AnswerForm,
        'answer4': AnswerForm,
    }


class PlayerForm(forms.ModelForm):
    class Meta:
        model   = Player
        exclude = ['user']
