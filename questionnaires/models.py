import datetime

from django.db import models
from django.utils import timezone

# Create your models here.


class Questionnaire(models.Model):
    title = models.CharField(max_length=200)
    about = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.title)

    def was_published_recently(self):
        return self.published_at >= timezone.now() - datetime.timedelta(days=1)


class Page(models.Model):
    page_order = models.IntegerField(default=0)
    page_score = models.IntegerField(default=0)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)

    class Meta:
        ordering = ['page_order']

    def __str__(self):
        return "{}".format(self.page_order)


class Question(models.Model):
    question_text = models.CharField(max_length=300)
    question_order = models.IntegerField(default=0)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text

    class Meta:
        ordering = ['question_order']


class Answer(models.Model):
    answer_text = models.CharField(max_length=100)
    answer_points = models.IntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer_text


class Result(models.Model):
    result_text = models.CharField(max_length=400)
    questionnaire = models.OneToOneField(Questionnaire, on_delete=models.CASCADE)