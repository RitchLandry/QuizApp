from django.contrib import admin
from django.contrib.admin.decorators import register
from django.contrib.admin.sites import site
from question.models import Question,Answer

# Register your models here.

class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer)