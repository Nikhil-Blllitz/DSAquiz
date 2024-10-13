from django.contrib import admin
from .models import Question, Answer, QuizResult, Attempt

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4  # Allows adding 4 additional answer options

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text',)  # Display question text in the list view
    search_fields = ('question_text',)  # Enable searching by question text
    inlines = [AnswerInline]  # Enable inline editing of answers
    fieldsets = (
        (None, {
            'fields': ('question_text',)
        }),
    )

class AttemptInline(admin.TabularInline):
    model = Attempt
    extra = 0  # No extra attempts by default
    # Display the question and selected answer
    fields = ('question', 'selected_answer')
    readonly_fields = ('question', 'selected_answer')  # Make these fields read-only

class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('name', 'usn', 'score', 'time_taken', 'created_at')  # Display relevant fields
    search_fields = ('name', 'usn', 'college_email')  # Enable searching by these fields
    inlines = [AttemptInline]  # Show attempts inline for each quiz result

# Register the models
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuizResult, QuizResultAdmin)
admin.site.register(Attempt)  # Register the Attempt model
