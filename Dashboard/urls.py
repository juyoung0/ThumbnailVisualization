from django.conf.urls import url
from . import views, views2, views3, views4

urlpatterns = [
    url(r'^study2$', views.main, name='main'),
    url(r'^study2/thumbnail$', views.show_thumbnail, name='thumbnail'),
    url(r'^study2/correlation$', views.stat_correlation, name='correlation'),
    url(r'^study2/anova$', views.stat_anova, name='anova'),
    url(r'^study2/result$', views.stat_result, name='result'),
    url(r'^study2/change_attention/$', views.change_attention, name='attention'),
    url(r'^study2/participant$', views.stat_participant, name='participant'),
    url(r'^study3$', views2.main, name='main2'),
    url(r'^study3/tn$', views2.show_tn, name='tndes'),
    url(r'^study3/thumbnail$', views2.show_thumbnail, name='thumbnail2'),
    url(r'^study3/participant$', views2.stat_participant, name='participant2'),
    url(r'^study4_old$', views3.main, name='main3'),
    url(r'^study4_old/tn$', views3.show_tn, name='tn'),
    url(r'^study4_old/participant$', views3.stat_participant, name='participant3'),
    url(r'^study4_old/thumbnail$', views3.show_thumbnail, name='thumbnail3'),
    url(r'^study4$', views4.main, name='main4'),
    url(r'^study4/result$', views4.stat_result, name='result4'),
    url(r'^study4/participant$', views4.stat_participant, name='participant4'),
]