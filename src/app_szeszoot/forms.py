#!/usr/bin/python3.7
from django import forms
from betterforms.multiform import MultiModelForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
)
from .models import (
    Game,
    Quiz,
    Question,
    Answer,
    Player,
)
from django.forms.fields import validators


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
        model  = Quiz
        fields = '__all__'


class QuestionForm(forms.ModelForm):
    class Meta:
        model   = Question
        exclude = ['quiz', 'image']


class CorrectAnswerForm(forms.ModelForm):
    answer_content = forms.CharField(max_length=256, label='Correct answer')

    class Meta:
        model  = Answer
        fields = ['answer_content']


class InorrectAnswerForm(forms.ModelForm):
    answer_content = forms.CharField(max_length=256, label='Inorrect answer')

    class Meta:
        model  = Answer
        fields = ['answer_content']


class QuestionAnswerForm(MultiModelForm):
    form_classes = {
        'question': QuestionForm,
        'answer1': CorrectAnswerForm,
        'answer2': InorrectAnswerForm,
        'answer3': InorrectAnswerForm,
        'answer4': InorrectAnswerForm,
    }


class PlayerForm(forms.ModelForm):
    nickname = forms.CharField(
        max_length=32,
        validators=[validators.RegexValidator(
            regex='^[a-zA-Z0-9_]*$',
            message='Only underscores (_) and  alphanumeric (a-z, A-Z, 0-9) characters are allowed.'
        )],
    )
    game     = forms.ModelChoiceField(queryset=Game.objects.all(), widget=forms.NumberInput, label='Game id')

    class Meta:
        model   = Player
        exclude = ['user']
