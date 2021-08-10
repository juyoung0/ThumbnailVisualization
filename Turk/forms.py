from django import forms
from .models import RankAnswer, PredictAnswer, ScoreAnswer, CompareAnswer

class RankForm(forms.ModelForm):
    class Meta:
        model = RankAnswer
        exclude = ['age', 'gender', 'isFinish', 'session_id', 'vis',
                   'token', 'attention', 'isFinished', 'education', 'news', 'start', 'finish', 'time']

class InfoForm(forms.ModelForm):
    class Meta:
        model = RankAnswer
        fields = ['age', 'gender', 'education', 'news', 'vis']

class InfoForm2(forms.ModelForm):
    class Meta:
        model = PredictAnswer
        fields = ['age', 'gender', 'education', 'news', 'vis', 'turkID']

class PredictForm(forms.ModelForm):
    class Meta:
        model = PredictAnswer
        exclude = ['age', 'gender', 'isFinish', 'session_id', 'vis', 'turkID',
                   'token', 'isFinished', 'education', 'news', 'start', 'finish', 'time']

class ScoreForm(forms.ModelForm):
    class Meta:
        model = ScoreAnswer
        exclude = ['age', 'gender', 'isFinish', 'session_id', 'vis', 'turkID',
                   'token', 'isFinished', 'education', 'news', 'start', 'finish', 'time']

class InfoForm3(forms.ModelForm):
    class Meta:
        model = ScoreAnswer
        fields = ['age', 'gender', 'education', 'news', 'vis', 'turkID']

class CompareForm(forms.ModelForm):
    class Meta:
        model = CompareAnswer
        exclude = ['age', 'gender', 'isFinish', 'session_id', 'vis', 'turkID',
                   'token', 'isFinished', 'education', 'news', 'start', 'finish', 'time']

class InfoForm4(forms.ModelForm):
    class Meta:
        model = CompareAnswer
        fields = ['age', 'gender', 'education', 'news', 'vis', 'turkID']