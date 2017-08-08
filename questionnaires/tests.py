import datetime

from django.utils import timezone
from django.test import TestCase

from .models import Questionnaire

# Create your tests here.


class QuestionnaireModelTests(TestCase):

    def questionnaire_was_published_recently(self):

        time = timezone.now() + datetime.timedelta(days=30)
        future_questionnaire = Questionnaire(published_at=time)
        self.assertIs(future_questionnaire.was_published_recently(), False)
