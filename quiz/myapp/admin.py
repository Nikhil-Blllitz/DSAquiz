from django.contrib import admin
from .models import Question, Answer, QuizResult

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text',)
    search_fields = ('question_text',)
    inlines = [AnswerInline]
    fieldsets = (
        (None, {
            'fields': ('question_text',)
        }),
    )

admin.site.register(Question, QuestionAdmin)
admin.site.register(QuizResult)  # Register the QuizResult model
