from quiz.models import Quiz
from django.db import models
from django.shortcuts import render
from question.models import Answer, Question
from result.models import Result
from django.views.generic import ListView
from django.http import JsonResponse
# Create your views here.

class QuizListView(ListView):
    model = Quiz
    template_name = 'quiz/main.html' 

def quiz_view(request,pk):
    quizes = Quiz.objects.get(pk=pk)
    return render(request, 'quiz/quiz.html', {'obj':quizes})

def quiz_data_view(request,pk):
    quizes = Quiz.objects.get(pk=pk)
    questions = []
    for q in quizes.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})
    return JsonResponse({'data':questions,'time':quizes.time,})

def save_quiz_view(request,pk):
    # print(request.POST)
    if request.is_ajax():
        questions = []
        data = request.POST
        data_ = dict(data.lists())
        
        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            print('key: ',k)
            question = Question.objects.get(text=k)
            questions.append(question)
        print(questions)

        user =request.user
        quiz = Quiz.objects.get(pk=pk)

        score = 0
        multiplier = 100 / quiz.number_of_questions
        results = []
        correct_answer = None

        for q in questions:
            ans_selected = request.POST.get(q.text)
            if ans_selected != "":
                question_ans = Answer.objects.filter(question=q)
                for a in question_ans:
                    if ans_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text
                results.append({str(q): {'correct_answer': correct_answer,'answered': ans_selected}})
            else:
                results.append({str(q):'not answered'})
        score_ = score * multiplier
        Result.objects.create(quiz=quiz,user=user,score=score_)

        if score_ >= quiz.min_score:
            return JsonResponse({'passed':True,'score':score_,'results':results})
        else:       
            return JsonResponse({'passed':False,'score':score_,'results':results})

