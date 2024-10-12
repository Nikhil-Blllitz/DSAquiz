from django.shortcuts import render, redirect
from .models import Question, QuizResult
from django.db import IntegrityError

def start_quiz(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        usn = request.POST.get('usn')
        department = request.POST.get('department')
        college_email = request.POST.get('college_email')

        # Check if the USN already exists
        if QuizResult.objects.filter(usn=usn).exists():
            error_message = "This USN has already been used. Please enter a unique USN."
            return render(request, 'quiz/start_quiz.html', {'error_message': error_message})

        request.session['quiz_name'] = name  # Store the name in the session
        request.session['usn'] = usn  # Store the USN in the session
        request.session['department'] = department  # Store department in the session
        request.session['college_email'] = college_email  # Store college email in the session
        return redirect('quiz')  # Redirect to the quiz view

    return render(request, 'quiz/start_quiz.html')  # Render the start quiz form
def quiz_view(request):
    questions = Question.objects.order_by('?')[:10].prefetch_related('answers')
    return render(request, 'quiz/quiz.html', {'questions': questions})

def submit_quiz(request):
    if request.method == 'POST':
        score = 0
        name = request.session.get('quiz_name', 'Anonymous')  # Get the name from the session
        usn = request.session.get('usn')  # Get the USN from the session

        # Calculate the score
        for question in Question.objects.order_by('?')[:10].prefetch_related('answers'):
            selected_answer_id = request.POST.get(f'question_{question.id}')
            if selected_answer_id:
                answer = question.answers.get(id=selected_answer_id)
                if answer.is_correct:
                    score += 1
        
        # Store the quiz result with the name and score
        QuizResult.objects.create(name=name, usn=usn, score=score)

        return render(request, 'quiz/result.html', {'score': score})
    
    return redirect('quiz')  # Redirect to quiz if not a POST request