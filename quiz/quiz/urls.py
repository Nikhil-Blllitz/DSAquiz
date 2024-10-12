from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('start_quiz/', views.start_quiz, name='start_quiz'),  # New URL for starting the quiz
    path('quiz/', views.quiz_view, name='quiz'),                # Existing quiz URL
    path('submit/', views.submit_quiz, name='submit_quiz'),     # Existing submit quiz URL
    path('', views.start_quiz, name='home'),                    # Redirect to start quiz on the home URL
]
