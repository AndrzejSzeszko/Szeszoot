#!/usr/bin/python3.7
from .models import (
    Quiz,
    Question,
    Answer,
)
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
import json


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['pk', 'answer_content', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    answer_set = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['pk', 'question_content', 'image', 'answer_set']


class QuizSerializer(serializers.ModelSerializer):
    question_set = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['pk', 'title', 'question_set']
