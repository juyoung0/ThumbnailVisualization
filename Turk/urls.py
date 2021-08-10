from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^startRank', views.start_rank, name='turk'),
    url(r'^startPredict', views.start_predict, name='turk2'),
    url(r'^startScore', views.start_score, name='turk3'),
    url(r'^startCompare', views.start_compare, name='turk4'),
    url(r'^informationRank', views.submit_rank_information, name='info'),
    url(r'^informationPredict', views.submit_predict_information, name='info2'),
    url(r'^informationScore', views.submit_score_information, name='info3'),
    url(r'^informationCompare', views.submit_compare_information, name='info4'),
    url(r'^rank', views.study_rank, name='rank'),
    url(r'^predict', views.study_predict, name='predict'),
    url(r'^score', views.study_score, name='score'),
    url(r'^compare', views.study_compare, name='compare'),
    url(r'^submit_rank_answer', views.submit_rank_answer, name='submit'),
    url(r'^submit_predict_answer', views.submit_predict_answer, name='submit2'),
    url(r'^submit_score_answer', views.submit_score_answer, name='submit3'),
    url(r'^submit_compare_answer', views.submit_compare_answer, name='submit4'),
]

