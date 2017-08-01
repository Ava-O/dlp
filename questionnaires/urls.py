from django.conf.urls import include, url

from . import views


app_name = 'questionnaires'
#
# urlpatterns = [
#     url(r'^$', views.IndexView.as_view(), name='index'),
#     url(r'^(?P<pk>[0-9]+)/$', views.QuestionnaireDetailView.as_view(), name='first_page'),
#     url(r'^(?P<page_id>[0-9]+)/choice/$', views.choice, name='choice'),
#     url(r'^(?P<pk>[0-9]+)/$', views.ResultsView.as_view(), name='result')
# ]

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.QuestionnaireDetailView.as_view(), name='first_page'),
    url(r'^(?P<pk>[0-9]+)/page/(?P<page_pk>[0-9]+)$', views.PageDetailView.as_view(), name='page'),
    url(r'^(?P<pk>[0-9]+)/result$', views.ResultsView.as_view(), name='result')
]