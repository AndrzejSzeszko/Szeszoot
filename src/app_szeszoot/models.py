from django.db import models
from django.contrib.auth import (
    settings,
    models as auth_models
)


class CustomUser(auth_models.AbstractUser):
    email = models.EmailField(unique=True)


class Quiz(models.Model):
    title       = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=256)


class Question(models.Model):
    question_content = models.CharField(max_length=256)
    image            = models.ImageField(upload_to='questions_images', null=True, blank=True)
    quiz             = models.ForeignKey(Quiz, on_delete=models.CASCADE)


class Answer(models.Model):
    question       = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_content = models.CharField(max_length=256)
    is_correct     = models.BooleanField(default=False)
    player         = models.ManyToManyField('Player')


class Game(models.Model):
    PIN = models.PositiveIntegerField(null=True)


class Player(models.Model):
    nickname = models.CharField(max_length=32, unique=True)
    game     = models.ForeignKey(Game, on_delete=models.CASCADE)
    user     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
