from django.contrib import admin
from .models import Questionnaire, Page, Question, Answer


class PageInline(admin.StackedInline):
    model = Page
    extra = 3


class QuestionnaireAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title']}),
        (None, {'fields': ['about']}),
    ]
    inlines = [PageInline]

    list_display = ('title', 'published_at')


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 3


class PageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['page_order']}),
        (None, {'fields': ['questionnaire']})
    ]
    inlines = [QuestionInline]


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        (None, {'fields': ['page']})
    ]
    inlines = [AnswerInline]


class AnswerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['answer_text']}),
        (None, {'fields': ['answer_points']}),
        (None, {'fields': ['question']})
    ]


admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)

