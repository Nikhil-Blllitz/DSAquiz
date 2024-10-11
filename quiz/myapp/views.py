from django.shortcuts import render
from .models import Question

def quiz_view(request):
    questions = Question.objects.order_by('?')[:10].prefetch_related('answers')
    return render(request, 'quiz/quiz.html', {'questions': questions})

def submit_quiz(request):
    if request.method == 'POST':
        score = 0
        for question in Question.objects.order_by('?')[:10].prefetch_related('answers'):
            selected_answer_id = request.POST.get(f'question_{question.id}')
            if selected_answer_id:
                answer = question.answers.get(id=selected_answer_id)
                if answer.is_correct:
                    score += 1
        return render(request, 'quiz/result.html', {'score': score})
    return render(request, 'quiz/quiz.html')
