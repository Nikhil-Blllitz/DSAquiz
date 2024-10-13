from django.db import models

class Question(models.Model):
    question_text = models.TextField()

    def __str__(self):
        return self.question_text

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class QuizResult(models.Model):
    name = models.CharField(max_length=100)  # Store the user's name
    usn = models.CharField(max_length=20, unique=True)  # Add USN field
    time_taken = models.IntegerField(default=0)
    department = models.CharField(max_length=100)  # Add Department field
    college_email = models.EmailField(max_length=255)  # Add College Mail ID field
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.score} on {self.created_at}"

class Attempt(models.Model):
    quiz_result = models.ForeignKey(QuizResult, related_name='attempts', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quiz_result.name} - {self.question.question_text}: {self.selected_answer.text}"
