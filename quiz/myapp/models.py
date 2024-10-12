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
    department = models.CharField(max_length=100)  # Add Department field
    college_email = models.EmailField(max_length=255)  # Add College Mail ID field
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.score} on {self.created_at}"
