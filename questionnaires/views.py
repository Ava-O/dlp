from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, render_to_response
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Questionnaire, Page, Question, Answer, Result


class IndexView(generic.ListView):
    template_name = 'questionnaire/index.html'
    context_object_name = 'latest_questionnaire_list'

    ''' display questionnaire list ordered by the an ascending published date'''
    def get_queryset(self):
        return Questionnaire.objects.filter(
            published_at__lte=timezone.now()
        ).order_by('-published_at')[:5].reverse()


class QuestionnaireDetailView(generic.DetailView):
    model = Questionnaire
    template_name = 'questionnaire/page.html'

    # def get_context_data(self, **kwargs):
    #     context = super(QuestionnaireDetailView, self).get_context_data(**kwargs)
    #     questionnaire = context['questionnaire']
    #     page = questionnaire.page_set.order_by('page_order').first()
    #     context['page'] = page
    #     self.request.session['page_score'] = 0
    #     context['page_score'] = 0
    #     self.request.session['best_answers'] = []
    #     self.request.session['visited_pages'] = []
    #     return context
    def get(self, request, *args, **kwargs):
        import ipdb;
        ipdb.set_trace()
        questionnaire = self.get_object()
        first_page = questionnaire.page_set.order_by('page_order').first()
        self.request.session.flush()
        self.request.session['page_score'] = 0
        self.request.session['best_answers'] = []
        self.request.session['visited_pages'] = []
        return HttpResponseRedirect(reverse("questionnaires:page", kwargs={"pk": questionnaire.pk,
                                                                                 "page_pk": first_page.pk}))


class ResultsView(generic.DetailView):
    model = Questionnaire
    template_name = 'questionnaire/results.html'


def get_max_score(questionnaire):
    answers = []
    vals = []
    all_answers_points = []
    max_list = []

    for page in questionnaire.page_set.all():
        for question in page.question_set.all():
            answers.append(question.answer_set.all())

    for answer in answers:
        vals.append(answer.values())

    for queryset in vals:
        for dictionary in queryset:
            for key in dictionary:
                if key == 'answer_points':
                    all_answers_points.append(dictionary[key])
        max_list.append(max(all_answers_points))

    max_score = sum(max_list)

    return max_score


def get_next_page(current_page):
    ordered_pages = current_page.questionnaire.page_set.all().order_by('page_order')
    return ordered_pages.filter(page_order__gt=current_page.page_order).first()


def get_a_question_with_wrong_answer(answer_set):

    better_answers = {}

    for answer in answer_set:
        if answer.answer_points is not 10:
            #get the Answer object related to the answer
            ans = Answer.objects.select_related('question').get(id=answer.id)
            #get the related question for the Answer object
            related_question = ans.question
            a = related_question.answer_set.all()
            for answ in a:
                if answ.answer_points == 10:
                    better_answers['q_best_answer'] = answ.answer_text
            better_answers['q_text'] = related_question.question_text
            better_answers['q_number'] = related_question.id

            #need to get all answer object related to the related question
            return better_answers


#register user answers
class PageDetailView(generic.DetailView):

    model = Page

    def get(self, request, *args, **kwargs):
        import ipdb;
        ipdb.set_trace()
        page = self.get_object()
        next_page = get_next_page(page)
        if page.page_order not in request.session['visited_pages']:
            request.session['visited_pages'].append(page.page_order)

        context = {'page': page, 'questionnaire': page.questionnaire, 'page_score': request.session['page_score'],
                   'best_answers': request.session['best_answers'], 'next_page': next_page
                   }

        if next_page.page_order <= request.session['visited_pages'][-1] + 1:
            return render(request, 'questionnaire/page.html', context)
        else:
            raise Http404("Page can't be accessed")

    def post(self, request, *args, **kwargs):
        import ipdb;
        ipdb.set_trace()
        page = self.get_object()
        next_page = get_next_page(page)
        answers_list = []
        for question in page.question_set.all():
            selected_answers = question.answer_set.get(pk=request.POST['answer{}'.format(question.id)])
            request.session['page_score'] += selected_answers.answer_points
            answers_list.append(selected_answers)
        for answer in answers_list:
            if answer is not None:
                diff_q = get_a_question_with_wrong_answer(answers_list)
        if diff_q:
            if diff_q not in request.session['best_answers']:
                request.session['best_answers'].append(diff_q)

        if next_page:
            return HttpResponseRedirect(
                reverse("questionnaires:page", kwargs={"pk": next_page.questionnaire.pk, "page_pk": next_page.pk}))
        else:
            return HttpResponseRedirect(
                reverse("questionnaires:result", kwargs={"pk": page.questionnaire.pk, "page_pk": page.pk}))




