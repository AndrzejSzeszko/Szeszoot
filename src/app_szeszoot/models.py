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

    def __str__(self):
        return self.title


class Question(models.Model):
    question_content = models.CharField(max_length=256)
    image            = models.ImageField(upload_to='questions_images', null=True, blank=True)
    quiz             = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_content


class Answer(models.Model):
    question       = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_content = models.CharField(max_length=256)
    is_correct     = models.BooleanField(default=False)
    player         = models.ManyToManyField('Player', through='PlayerAnswer')

    def __str__(self):
        return self.answer_content


class Game(models.Model):
    PIN  = models.PositiveIntegerField(null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)


class Player(models.Model):
    nickname = models.CharField(max_length=32, unique=True)
    game     = models.ForeignKey(Game, on_delete=models.CASCADE)
    user     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nickname


class PlayerAnswer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    points = models.FloatField()
