from django.db import models
from django.contrib.auth import settings


class Quiz(models.Model):
    title = models.CharField(max_length=32)


class Question(models.Model):
    question_content = models.CharField(max_length=256)
    image = models.ImageField(upload_to='questions_images', null=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_right = models.BooleanField(default=False)
    player = models.ManyToManyField('Player')


class Game(models.Model):
    PIN = models.PositiveIntegerField()


class Player(models.Model):
    nickname = models.CharField(max_length=32)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
