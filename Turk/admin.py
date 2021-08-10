from django.contrib import admin
from .models import RankAnswer, PredictAnswer, ScoreAnswer, CompareAnswer

# Register your models here.
admin.site.register(RankAnswer)
admin.site.register(PredictAnswer)
admin.site.register(ScoreAnswer)
admin.site.register(CompareAnswer)