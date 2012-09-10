from django.contrib import admin
from labgeeksrpg.delphi.models import Question, Answer


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'question')
    fields = ('question', 'more_info')


admin.site.register(Question, QuestionAdmin)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'question', 'is_best')
    fields = ('answer', 'is_best')


admin.site.register(Answer, AnswerAdmin)
