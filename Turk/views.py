from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from Turk.forms import RankForm, InfoForm, PredictForm, InfoForm2, InfoForm3, ScoreForm, CompareForm, InfoForm4
from Turk.models import RankAnswer, PredictAnswer, ScoreAnswer, CompareAnswer
from django.views.decorators.csrf import csrf_exempt
import uuid

@csrf_exempt
def start_rank(request):
    num_results = RankAnswer.objects.all().count()
    print(num_results)
    # if num_results>=78:
    #     return render(request, 'Turk/full.html')

    if not request.session.session_key:
        request.session.create()
    session_id = request.session.session_key
    context = {}
    context['session_id'] = session_id
    form = InfoForm()
    return render(request, 'turkMaster.html', {'form' : form})

@csrf_exempt
def start_predict(request):
    num_results = PredictAnswer.objects.all().count()
    print(num_results)

    # if num_results > 350:
    #     return render(request, 'Turk/full.html')

    if not request.session.session_key:
        request.session.create()

    session_id = request.session.session_key
    context = {}
    context['session_id'] = session_id
    form = InfoForm2()
    return render(request, 'turkMaster2.html', {'form' : form})

@csrf_exempt
def start_score(request):
    if not request.session.session_key:
        request.session.create()
    session_id = request.session.session_key
    context = {}
    context['session_id'] = session_id
    form = InfoForm3()
    return render(request, 'turkMaster3.html', {'form' : form})

@csrf_exempt
def start_compare(request):
    num_results = CompareAnswer.objects.all().count()
    print(num_results)
    # if num_results > 110:
    #     return render(request, 'Turk/full.html')

    if not request.session.session_key:
        request.session.create()
    session_id = request.session.session_key
    context = {}
    context['session_id'] = session_id
    form = InfoForm4()
    return render(request, 'turkMaster4.html', {'form' : form})

@csrf_exempt
def submit_rank_information(request):
    if request.method == 'POST':
        #save information
        form = InfoForm(request.POST)
        if form.is_valid():
            session_id = request.session.session_key
            num_results = RankAnswer.objects.filter(session_id=session_id).count()

            if num_results > 0:
                return render(request, 'Turk/already.html')

            answer = RankAnswer(session_id=session_id)
            answer.age = form.cleaned_data["age"]
            answer.gender = form.cleaned_data["gender"]
            answer.education = form.cleaned_data["education"]
            answer.news = form.cleaned_data["news"]
            answer.vis = form.cleaned_data["vis"]
            answer.save()
            return render(request, 'Turk/rank.html')
        else:
            context = {}
            context["message"] = "Input is not valid"
            context["form"] = InfoForm()
            return render(request, 'Turk/information.html', context)
    else:
        context = {}
        context["message"] = "Input is not valid"
        context["form"] = InfoForm()
        return render(request, 'Turk/information.html', context)

@csrf_exempt
def submit_predict_information(request):
    if request.method == 'POST':
        #save information
        form = InfoForm2(request.POST)
        if form.is_valid():
            session_id = request.session.session_key
            num_results = PredictAnswer.objects.filter(session_id=session_id).count()

            if num_results > 0:
                return render(request, 'Turk/already.html')

            answer = PredictAnswer(session_id=session_id)
            answer.age = form.cleaned_data["age"]
            answer.gender = form.cleaned_data["gender"]
            answer.education = form.cleaned_data["education"]
            answer.news = form.cleaned_data["news"]
            answer.vis = form.cleaned_data["vis"]
            answer.turkID = form.cleaned_data["turkID"]
            answer.save()
            context = {}
            context["num"] = answer.id % 8 + 1

            context["message"] = True
            return render(request, 'Turk/predict.html', context)
        else:
            context = {}
            context["message"] = False
            context["form"] = InfoForm2()

            return render(request, 'Turk/information2.html', context)
    else:
        context = {}
        context["message"] = False
        context["form"] = InfoForm2()
        return render(request, 'Turk/information2.html', context)

@csrf_exempt
def submit_score_information(request):
    descriptions = {'1':[39,40,41,42, 43], '2':[39,40,41,42, 43], '3':[39,40,41,42, 43], '4':[39,40,41,42, 43], '5':[39,40,41,42, 43], '6':[39,40,41,42, 43], '7':[39,40,41,42, 43], '8':[39,40,41,42, 43]}
    if request.method == 'POST':
        #save information
        form = InfoForm3(request.POST)
        if form.is_valid():
            session_id = request.session.session_key
            num_results = ScoreAnswer.objects.filter(session_id=session_id).count()
            if num_results > 0:
                return render(request, 'Turk/already.html')

            answer = ScoreAnswer(session_id=session_id)
            answer.age = form.cleaned_data["age"]
            answer.gender = form.cleaned_data["gender"]
            answer.education = form.cleaned_data["education"]
            answer.news = form.cleaned_data["news"]
            answer.vis = form.cleaned_data["vis"]
            answer.turkID = form.cleaned_data["turkID"]
            answer.save()

            context = {}
            tn_num = answer.id % 8 + 1
            context['num'] = tn_num

            for idx in range(5):
                #context["des"+str(idx+1)] = PredictAnswer.objects.get(id=descriptions[str(tn_num)][idx]).des
                context["des" + str(1)] = "Maybe, it says that economics and safety are related with public trust. These day, people's life become happier, they don't trust public."
                context["des" + str(2)] = "The trust of the government has been raised and fall by events from 1960-2010. There were two main rises in 1980s and 1990s and peak in 2000s."
                context["des" + str(3)] = "Maybe evaluate the trump's politic actions and show an approval rating about that."
                context["des" + str(4)] = "This article shows overall trends of public trust in Government. It shows historic lows in public trust in the government."
                context["des" + str(5)] = "The public trust of the U.S. government has been decreased from 1960. It remains historic lows showing only 18% after last increases after 9/11 terror"
            return render(request, 'Turk/score.html', context)
        else:
            context = {}
            context["message"] = "Input is not valid"
            context["form"] = InfoForm3()
            return render(request, 'Turk/information3.html', context)
    else:
        context = {}
        context["message"] = "Input is not valid"
        context["form"] = InfoForm3()
        return render(request, 'Turk/information3.html', context)

@csrf_exempt
def submit_compare_information(request):
    if request.method == 'POST':
        #save information
        form = InfoForm4(request.POST)
        if form.is_valid():
            session_id = request.session.session_key
            num_results = CompareAnswer.objects.filter(session_id=session_id).count()
            if num_results > 0:
               return render(request, 'Turk/already.html')

            answer = CompareAnswer(session_id=session_id)
            answer.age = form.cleaned_data["age"]
            answer.gender = form.cleaned_data["gender"]
            answer.education = form.cleaned_data["education"]
            answer.news = form.cleaned_data["news"]
            answer.vis = form.cleaned_data["vis"]
            answer.turkID = form.cleaned_data["turkID"]
            answer.save()

            return render(request, 'Turk/compare.html')
        else:
            context = {}
            context["message"] = "Input is not valid"
            context["form"] = InfoForm4()
            return render(request, 'Turk/information4.html', context)
    else:
        context = {}
        context["message"] = "Input is not valid"
        context["form"] = InfoForm4()
        return render(request, 'Turk/information4.html', context)

@csrf_exempt
def submit_rank_answer(request):
    attr_num = 5
    # POST 요청이면 폼 데이터를 처리한다
    if request.method == 'POST':
        # 폼 인스턴스를 생성하고 요청에 의한 데이타로 채운다 (binding):
        form = RankForm(request.POST)
        session_id = request.session.session_key
        randomString = str(uuid.uuid4()).replace("-", "")
        # 폼이 유효한지 체크한다:
        if form.is_valid():
            #answer = RankAnswer(session_id=session_id)
            answer = RankAnswer.objects.get(session_id=session_id)
            answer.token = randomString
            answer.a1g1t1 = form.cleaned_data['a1g1t1']
            answer.a1g1t2 = form.cleaned_data['a1g1t2']
            answer.a1g1t3 = form.cleaned_data['a1g1t3']
            answer.a1g1t4 = form.cleaned_data['a1g1t4']
            answer.a1g1t5 = form.cleaned_data['a1g1t5']
            answer.a1g1t6 = form.cleaned_data['a1g1t6']
            answer.a1g1t7 = form.cleaned_data['a1g1t7']
            answer.a1g1t8 = form.cleaned_data['a1g1t8']
            answer.a1g1t9 = form.cleaned_data['a1g1t9']
            answer.a1g1t10 = form.cleaned_data['a1g1t10']
            answer.a1g1t11 = form.cleaned_data['a1g1t11']
            answer.a1g1t12 = form.cleaned_data['a1g1t12']
            answer.a1g1t13 = form.cleaned_data['a1g1t13']
            answer.a1g1t14 = form.cleaned_data['a1g1t14']
            answer.a1g1t15 = form.cleaned_data['a1g1t15']
            answer.a1g1t16 = form.cleaned_data['a1g1t16']
            answer.a1g1t17 = form.cleaned_data['a1g1t17']
            answer.a1g2t1 = form.cleaned_data['a1g2t1']
            answer.a1g2t2 = form.cleaned_data['a1g2t2']
            answer.a1g2t3 = form.cleaned_data['a1g2t3']
            answer.a1g2t4 = form.cleaned_data['a1g2t4']
            answer.a1g2t5 = form.cleaned_data['a1g2t5']
            answer.a1g2t6 = form.cleaned_data['a1g2t6']
            answer.a1g2t7 = form.cleaned_data['a1g2t7']
            answer.a1g2t8 = form.cleaned_data['a1g2t8']
            answer.a1g2t9 = form.cleaned_data['a1g2t9']
            answer.a1g2t10 = form.cleaned_data['a1g2t10']
            answer.a1g2t11 = form.cleaned_data['a1g2t11']
            answer.a1g2t12 = form.cleaned_data['a1g2t12']
            answer.a1g2t13 = form.cleaned_data['a1g2t13']
            answer.a1g2t14 = form.cleaned_data['a1g2t14']
            answer.a1g2t15 = form.cleaned_data['a1g2t15']
            answer.a1g2t16 = form.cleaned_data['a1g2t16']
            answer.a1g2t17 = form.cleaned_data['a1g2t17']
            answer.a1g3t1 = form.cleaned_data['a1g3t1']
            answer.a1g3t2 = form.cleaned_data['a1g3t2']
            answer.a1g3t3 = form.cleaned_data['a1g3t3']
            answer.a1g3t4 = form.cleaned_data['a1g3t4']
            answer.a1g3t5 = form.cleaned_data['a1g3t5']
            answer.a1g3t6 = form.cleaned_data['a1g3t6']
            answer.a1g3t7 = form.cleaned_data['a1g3t7']
            answer.a1g3t8 = form.cleaned_data['a1g3t8']
            answer.a1g3t9 = form.cleaned_data['a1g3t9']
            answer.a1g3t10 = form.cleaned_data['a1g3t10']
            answer.a1g3t11 = form.cleaned_data['a1g3t11']
            answer.a1g3t12 = form.cleaned_data['a1g3t12']
            answer.a1g3t13 = form.cleaned_data['a1g3t13']
            answer.a1g3t14 = form.cleaned_data['a1g3t14']
            answer.a1g3t15 = form.cleaned_data['a1g3t15']
            answer.a1g3t16 = form.cleaned_data['a1g3t16']
            answer.a1g3t17 = form.cleaned_data['a1g3t17']
            answer.a1g4t1 = form.cleaned_data['a1g4t1']
            answer.a1g4t2 = form.cleaned_data['a1g4t2']
            answer.a1g4t3 = form.cleaned_data['a1g4t3']
            answer.a1g4t4 = form.cleaned_data['a1g4t4']
            answer.a1g4t5 = form.cleaned_data['a1g4t5']
            answer.a1g4t6 = form.cleaned_data['a1g4t6']
            answer.a1g4t7 = form.cleaned_data['a1g4t7']
            answer.a1g4t8 = form.cleaned_data['a1g4t8']
            answer.a1g4t9 = form.cleaned_data['a1g4t9']
            answer.a1g4t10 = form.cleaned_data['a1g4t10']
            answer.a1g4t11 = form.cleaned_data['a1g4t11']
            answer.a1g4t12 = form.cleaned_data['a1g4t12']
            answer.a1g4t13 = form.cleaned_data['a1g4t13']
            answer.a1g4t14 = form.cleaned_data['a1g4t14']
            answer.a1g4t15 = form.cleaned_data['a1g4t15']
            answer.a1g4t16 = form.cleaned_data['a1g4t16']
            answer.a1g4t17 = form.cleaned_data['a1g4t17']
            answer.a1g5t1 = form.cleaned_data['a1g5t1']
            answer.a1g5t2 = form.cleaned_data['a1g5t2']
            answer.a1g5t3 = form.cleaned_data['a1g5t3']
            answer.a1g5t4 = form.cleaned_data['a1g5t4']
            answer.a1g5t5 = form.cleaned_data['a1g5t5']
            answer.a1g5t6 = form.cleaned_data['a1g5t6']
            answer.a1g5t7 = form.cleaned_data['a1g5t7']
            answer.a1g5t8 = form.cleaned_data['a1g5t8']
            answer.a1g5t9 = form.cleaned_data['a1g5t9']
            answer.a1g5t10 = form.cleaned_data['a1g5t10']
            answer.a1g5t11 = form.cleaned_data['a1g5t11']
            answer.a1g5t12 = form.cleaned_data['a1g5t12']
            answer.a1g5t13 = form.cleaned_data['a1g5t13']
            answer.a1g5t14 = form.cleaned_data['a1g5t14']
            answer.a1g5t15 = form.cleaned_data['a1g5t15']
            answer.a1g5t16 = form.cleaned_data['a1g5t16']
            answer.a1g5t17 = form.cleaned_data['a1g5t17']
            answer.a2g1t1 = form.cleaned_data['a2g1t1']
            answer.a2g1t2 = form.cleaned_data['a2g1t2']
            answer.a2g1t3 = form.cleaned_data['a2g1t3']
            answer.a2g1t4 = form.cleaned_data['a2g1t4']
            answer.a2g1t5 = form.cleaned_data['a2g1t5']
            answer.a2g1t6 = form.cleaned_data['a2g1t6']
            answer.a2g1t7 = form.cleaned_data['a2g1t7']
            answer.a2g1t8 = form.cleaned_data['a2g1t8']
            answer.a2g1t9 = form.cleaned_data['a2g1t9']
            answer.a2g1t10 = form.cleaned_data['a2g1t10']
            answer.a2g1t11 = form.cleaned_data['a2g1t11']
            answer.a2g1t12 = form.cleaned_data['a2g1t12']
            answer.a2g1t13 = form.cleaned_data['a2g1t13']
            answer.a2g1t14 = form.cleaned_data['a2g1t14']
            answer.a2g1t15 = form.cleaned_data['a2g1t15']
            answer.a2g1t16 = form.cleaned_data['a2g1t16']
            answer.a2g1t17 = form.cleaned_data['a2g1t17']
            answer.a2g2t1 = form.cleaned_data['a2g2t1']
            answer.a2g2t2 = form.cleaned_data['a2g2t2']
            answer.a2g2t3 = form.cleaned_data['a2g2t3']
            answer.a2g2t4 = form.cleaned_data['a2g2t4']
            answer.a2g2t5 = form.cleaned_data['a2g2t5']
            answer.a2g2t6 = form.cleaned_data['a2g2t6']
            answer.a2g2t7 = form.cleaned_data['a2g2t7']
            answer.a2g2t8 = form.cleaned_data['a2g2t8']
            answer.a2g2t9 = form.cleaned_data['a2g2t9']
            answer.a2g2t10 = form.cleaned_data['a2g2t10']
            answer.a2g2t11 = form.cleaned_data['a2g2t11']
            answer.a2g2t12 = form.cleaned_data['a2g2t12']
            answer.a2g2t13 = form.cleaned_data['a2g2t13']
            answer.a2g2t14 = form.cleaned_data['a2g2t14']
            answer.a2g2t15 = form.cleaned_data['a2g2t15']
            answer.a2g2t16 = form.cleaned_data['a2g2t16']
            answer.a2g2t17 = form.cleaned_data['a2g2t17']
            answer.a2g3t1 = form.cleaned_data['a2g3t1']
            answer.a2g3t2 = form.cleaned_data['a2g3t2']
            answer.a2g3t3 = form.cleaned_data['a2g3t3']
            answer.a2g3t4 = form.cleaned_data['a2g3t4']
            answer.a2g3t5 = form.cleaned_data['a2g3t5']
            answer.a2g3t6 = form.cleaned_data['a2g3t6']
            answer.a2g3t7 = form.cleaned_data['a2g3t7']
            answer.a2g3t8 = form.cleaned_data['a2g3t8']
            answer.a2g3t9 = form.cleaned_data['a2g3t9']
            answer.a2g3t10 = form.cleaned_data['a2g3t10']
            answer.a2g3t11 = form.cleaned_data['a2g3t11']
            answer.a2g3t12 = form.cleaned_data['a2g3t12']
            answer.a2g3t13 = form.cleaned_data['a2g3t13']
            answer.a2g3t14 = form.cleaned_data['a2g3t14']
            answer.a2g3t15 = form.cleaned_data['a2g3t15']
            answer.a2g3t16 = form.cleaned_data['a2g3t16']
            answer.a2g3t17 = form.cleaned_data['a2g3t17']
            answer.a2g4t1 = form.cleaned_data['a2g4t1']
            answer.a2g4t2 = form.cleaned_data['a2g4t2']
            answer.a2g4t3 = form.cleaned_data['a2g4t3']
            answer.a2g4t4 = form.cleaned_data['a2g4t4']
            answer.a2g4t5 = form.cleaned_data['a2g4t5']
            answer.a2g4t6 = form.cleaned_data['a2g4t6']
            answer.a2g4t7 = form.cleaned_data['a2g4t7']
            answer.a2g4t8 = form.cleaned_data['a2g4t8']
            answer.a2g4t9 = form.cleaned_data['a2g4t9']
            answer.a2g4t10 = form.cleaned_data['a2g4t10']
            answer.a2g4t11 = form.cleaned_data['a2g4t11']
            answer.a2g4t12 = form.cleaned_data['a2g4t12']
            answer.a2g4t13 = form.cleaned_data['a2g4t13']
            answer.a2g4t14 = form.cleaned_data['a2g4t14']
            answer.a2g4t15 = form.cleaned_data['a2g4t15']
            answer.a2g4t16 = form.cleaned_data['a2g4t16']
            answer.a2g4t17 = form.cleaned_data['a2g4t17']
            answer.a2g5t1 = form.cleaned_data['a2g5t1']
            answer.a2g5t2 = form.cleaned_data['a2g5t2']
            answer.a2g5t3 = form.cleaned_data['a2g5t3']
            answer.a2g5t4 = form.cleaned_data['a2g5t4']
            answer.a2g5t5 = form.cleaned_data['a2g5t5']
            answer.a2g5t6 = form.cleaned_data['a2g5t6']
            answer.a2g5t7 = form.cleaned_data['a2g5t7']
            answer.a2g5t8 = form.cleaned_data['a2g5t8']
            answer.a2g5t9 = form.cleaned_data['a2g5t9']
            answer.a2g5t10 = form.cleaned_data['a2g5t10']
            answer.a2g5t11 = form.cleaned_data['a2g5t11']
            answer.a2g5t12 = form.cleaned_data['a2g5t12']
            answer.a2g5t13 = form.cleaned_data['a2g5t13']
            answer.a2g5t14 = form.cleaned_data['a2g5t14']
            answer.a2g5t15 = form.cleaned_data['a2g5t15']
            answer.a2g5t16 = form.cleaned_data['a2g5t16']
            answer.a2g5t17 = form.cleaned_data['a2g5t17']
            answer.check1id = form.cleaned_data['check1id']
            answer.check2id = form.cleaned_data['check2id']
            answer.check1val1 = form.cleaned_data['check1val1']
            answer.check1val2 = form.cleaned_data['check1val2']
            answer.check1val3 = form.cleaned_data['check1val3']
            answer.check1val4 = form.cleaned_data['check1val4']
            answer.check1val5 = form.cleaned_data['check1val5']
            answer.check2val1 = form.cleaned_data['check2val1']
            answer.check2val2 = form.cleaned_data['check2val2']
            answer.check2val3 = form.cleaned_data['check2val3']
            answer.check2val4 = form.cleaned_data['check2val4']
            answer.check2val5 = form.cleaned_data['check2val5']
            answer.valid1 = form.cleaned_data['valid1']
            answer.valid2 = form.cleaned_data['valid2']
            answer.passTrap = form.cleaned_data['passTrap']
            check1id = form.cleaned_data['check1id']
            check2id = form.cleaned_data['check1id']
            answer.nonsenseNum = form.cleaned_data['nonsenseNum']

            # 중간에 attention check 틀렸는지 확인
            if answer.passTrap:
                answer.isFinish = True
                diff = 0
                for i in range(attr_num):
                    diff += abs( form.cleaned_data['a1g'+str(i+1)+'t'+str(check1id)] - form.cleaned_data['check1val'+str(i+1)] )

                for i in range(attr_num):
                    diff += abs(form.cleaned_data['a2g' + str(i + 1) + 't' + str(check2id)] - form.cleaned_data['check2val' + str(i + 1)])

                answer.attention = diff
                answer.save()
                time = answer.finish - answer.start
                answer.time = int(time.total_seconds())
                answer.save()
                # 랜덤토큰을 turk 사이트에 입력하여야 완료
                context = {'token':randomString}
                return render(request, 'Turk/finish.html', context)
            else:
                answer.isFinish = False
                answer.attention = 60
                answer.save()
                time = answer.finish - answer.start
                answer.time = int(time.total_seconds())
                answer.save()
                context = {'token':randomString}
                return render(request, 'Turk/fail.html', context)
        else:

            context = {'token':"Some Input is not exist"}
            context['form'] = form
            return render(request, 'Turk/finish.html', context)

@csrf_exempt
def submit_predict_answer(request):
    if request.method == 'POST':
        # 폼 인스턴스를 생성하고 요청에 의한 데이타로 채운다 (binding):
        form = PredictForm(request.POST)
        session_id = request.session.session_key
        randomString = str(uuid.uuid4()).replace("-", "")

        # 폼이 유효한지 체크한다:
        if form.is_valid():
            # answer = RankAnswer(session_id=session_id)
            answer = PredictAnswer.objects.get(session_id=session_id)
            answer.token = randomString
            answer.valid = form.cleaned_data['valid']
            answer.des = form.cleaned_data['des']
            answer.q1 = form.cleaned_data['q1']
            answer.q2 = form.cleaned_data['q2']
            answer.q3 = form.cleaned_data['q3']
            answer.q4 = form.cleaned_data['q4']
            answer.q5 = form.cleaned_data['q5']
            answer.q6 = form.cleaned_data['q6']
            answer.q7 = form.cleaned_data['q7']
            answer.tn = form.cleaned_data['tn']
            answer.passTrap = form.cleaned_data['passTrap']
            answer.width = form.cleaned_data['width']
            answer.height = form.cleaned_data['height']
            answer.help1 = form.cleaned_data['help1']
            answer.help2 = form.cleaned_data['help2']
            answer.help3 = form.cleaned_data['help3']

            # 중간에 attention check 틀렸는지 확인
            if answer.passTrap:
                answer.isFinish = True
                answer.save()
                time = answer.finish - answer.start
                answer.time = int(time.total_seconds())
                answer.save()
                # 랜덤토큰을 turk 사이트에 입력하여야 완료
                context = {'token': randomString}
                return render(request, 'Turk/finish.html', context)
            else:
                answer.isFinish = False
                answer.attention = 60
                answer.save()
                time = answer.finish - answer.start
                answer.time = int(time.total_seconds())
                answer.save()
                context = {'token': randomString}
                return render(request, 'Turk/fail.html', context)
        else:
            context = {'token': "Some Input is not exist"}
            context["form"] = form
            return render(request, 'Turk/finish.html', context)

@csrf_exempt
def submit_score_answer(request):
    if request.method == 'POST':
        # 폼 인스턴스를 생성하고 요청에 의한 데이타로 채운다 (binding):
        form = ScoreForm(request.POST)
        session_id = request.session.session_key
        randomString = str(uuid.uuid4()).replace("-", "")
        # 폼이 유효한지 체크한다:
        if form.is_valid():
            answer = ScoreAnswer.objects.get(session_id=session_id)
            answer.token = randomString
            answer.valid = form.cleaned_data['valid']
            answer.d1q1 = form.cleaned_data['d1q1']
            answer.d1q2 = form.cleaned_data['d1q2']
            answer.d1q3 = form.cleaned_data['d1q3']
            answer.d2q1 = form.cleaned_data['d2q1']
            answer.d2q2 = form.cleaned_data['d2q2']
            answer.d2q3 = form.cleaned_data['d2q3']
            answer.d3q1 = form.cleaned_data['d3q1']
            answer.d3q2 = form.cleaned_data['d3q2']
            answer.d3q3 = form.cleaned_data['d3q3']
            answer.d4q1 = form.cleaned_data['d4q1']
            answer.d4q2 = form.cleaned_data['d4q2']
            answer.d4q3 = form.cleaned_data['d4q3']
            answer.d5q1 = form.cleaned_data['d5q1']
            answer.d5q2 = form.cleaned_data['d5q2']
            answer.d5q3 = form.cleaned_data['d5q3']
            answer.tn = form.cleaned_data['tn']
            answer.passTrap = form.cleaned_data['passTrap']
            answer.width = form.cleaned_data['width']
            answer.height = form.cleaned_data['height']
            answer.check1val1 = form.cleaned_data['checkval1']
            answer.check1val2 = form.cleaned_data['checkval2']
            answer.check1val3 = form.cleaned_data['checkval3']
            answer.check1val4 = form.cleaned_data['checkval4']
            answer.check1val5 = form.cleaned_data['checkval5']

            # 중간에 attention check 틀렸는지 확인
            if answer.passTrap:
                answer.isFinish = True
                answer.save()
                time = answer.finish - answer.start
                answer.time = int(time.total_seconds())
                answer.save()
                # 랜덤토큰을 turk 사이트에 입력하여야 완료
                context = {'token': randomString}
                return render(request, 'Turk/finish.html', context)
            else:
                answer.isFinish = False
                answer.attention = 60
                answer.save()
                time = answer.finish - answer.start
                answer.time = int(time.total_seconds())
                answer.save()
                context = {'token': randomString}
                return render(request, 'Turk/fail.html', context)
        else:
            context = {'token': "Some Input is not exist"}
            context["form"] = form
            return render(request, 'Turk/finish.html', context)

@csrf_exempt
def submit_compare_answer(request):
    # POST 요청이면 폼 데이터를 처리한다
    if request.method == 'POST':
        # 폼 인스턴스를 생성하고 요청에 의한 데이타로 채운다 (binding):
        form = CompareForm(request.POST)
        session_id = request.session.session_key
        randomString = str(uuid.uuid4()).replace("-", "")
        # 폼이 유효한지 체크한다:
        if form.is_valid():
            #answer = RankAnswer(session_id=session_id)
            answer = CompareAnswer.objects.get(session_id=session_id)
            answer.token = randomString
            answer.q1 = form.cleaned_data['q1']
            answer.q2 = form.cleaned_data['q2']
            answer.q3a = form.cleaned_data['q3a']
            answer.q3b = form.cleaned_data['q3b']
            answer.q3c = form.cleaned_data['q3c']
            answer.q3d = form.cleaned_data['q3d']
            answer.width = form.cleaned_data['width']
            answer.height = form.cleaned_data['height']
            answer.passTrap = form.cleaned_data['passTrap']
            answer.trap = form.cleaned_data['trap']
            # 랜덤토큰을 turk 사이트에 입력하여야 완료
            if answer.passTrap:
                answer.isFinish = True
                answer.save()
                time = answer.finish - answer.start
                answer.time = int(time.total_seconds())
                answer.save()
                # 랜덤토큰을 turk 사이트에 입력하여야 완료
                context = {'token': randomString}
                return render(request, 'Turk/finish.html', context)
            else:
                answer.isFinish = False
                answer.attention = 60
                answer.save()
                time = answer.finish - answer.start
                answer.time = int(time.total_seconds())
                answer.save()
                context = {'token': randomString}
                return render(request, 'Turk/fail.html', context)

        else:
            context = {'token':"Some Input is not exist"}
            context['form'] = form
            return render(request, 'Turk/finish.html', context)

def study_rank(request):
    context = {}
    context["title"] = "this is rank"

    return render(request, 'Turk/rank.html', context)

def study_predict(request):
    context = {}
    context["title"] = "this is predict"
    return render(request, 'Turk/predict.html', context)

def study_score(request):
    context = {}
    context["title"] = "this is score"
    return render(request, 'Turk/score.html', context)

def study_compare(request):
    context = {}
    context["title"] = "this is compare"
    return render(request, 'Turk/compare.html', context)