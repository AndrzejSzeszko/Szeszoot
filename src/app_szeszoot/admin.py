from django.contrib import admin
from django.contrib.auth import get_user_model
from .forms import UpdateCustomUserForm
from .models import (
    Quiz,
    Question,
    Answer,
    Player,
    Game,
)


class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
    ]
    form = UpdateCustomUserForm


class QuizAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'title',
        'description',
    ]


class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'question_content',
        'image',
        'quiz',
    ]


class AnswerAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'question',
        'answer_content',
        'is_correct',
    ]


class PlayerAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'nickname',
        'game',
        'user',
    ]


class GameAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'PIN',
    ]


admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Player, PlayerAdmin)
