from django.shortcuts import render, redirect
from .models import Question, QuizResult, Attempt
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

        # Store quiz data in the session
        request.session['quiz_name'] = name
        request.session['usn'] = usn
        request.session['department'] = department
        request.session['college_email'] = college_email
        return redirect('quiz')  # Redirect to the quiz view

    return render(request, 'quiz/start_quiz.html')  # Render the start quiz form


def quiz_view(request):
    # Check if the quiz has already been taken by the user in this session
    if 'quiz_questions' in request.session:
        questions = Question.objects.filter(id__in=request.session['quiz_questions']).prefetch_related('answers')
    else:
        questions = Question.objects.order_by('?')[:10].prefetch_related('answers')
        request.session['quiz_questions'] = [q.id for q in questions]  # Store question IDs in session

    return render(request, 'quiz/quiz.html', {'questions': questions})


def submit_quiz(request):
    if request.method == 'POST':
        score = 0
        name = request.session.get('quiz_name', 'Anonymous')  # Get the name from the session
        usn = request.session.get('usn')  # Get the USN from the session
        time_taken = request.POST.get('time_taken')  # Get the time taken from the form
        department = request.session.get('department')
        college_email = request.session.get('college_email')

        # Retrieve question IDs from session
        question_ids = request.session.get('quiz_questions', [])
        
        # Create a new QuizResult object to store results
        quiz_result = QuizResult.objects.create(
            name=name,
            usn=usn,
            score=0,  # Initially set score to 0, will update later
            time_taken=time_taken,
            department=department,
            college_email=college_email
        )

        # Calculate the score and save attempts
        for question_id in question_ids:
            question = Question.objects.get(id=question_id)
            selected_answer_id = request.POST.get(f'question-{question.id}')
            if selected_answer_id:
                try:
                    answer = question.answers.get(id=selected_answer_id)
                    Attempt.objects.create(quiz_result=quiz_result, question=question, selected_answer=answer)

                    if answer.is_correct:
                        score += 1
                except answer.DoesNotExist:
                    continue  # If the answer doesn't exist, skip it

        # Update the score for the quiz result
        quiz_result.score = score
        quiz_result.save()

        # Clear the session to prevent re-submission
        request.session.pop('quiz_questions', None)  # Remove quiz questions from the session
        request.session.pop('quiz_name', None)  # Remove the name from the session
        request.session.pop('usn', None)  # Remove the USN from the session
        request.session.pop('department', None)  # Remove department from the session
        request.session.pop('college_email', None)  # Remove college email from the session

        # Redirect to the result view
        return redirect('result', quiz_result_id=quiz_result.id)  # Redirect to result view with quiz_result ID

    return redirect('start_quiz')  # Redirect to start_quiz if not a POST request


def result_view(request, quiz_result_id):
    # Fetch the quiz result using the ID
    quiz_result = QuizResult.objects.get(id=quiz_result_id)
    return render(request, 'quiz/result.html', {
        'score': quiz_result.score,
        'time_taken': quiz_result.time_taken,
        'attempts': quiz_result.attempts.all(),
    })
