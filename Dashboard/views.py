from django.shortcuts import render
import json, os, csv
import pandas as pd
import numpy as np
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import scipy.stats
from Turk.models import RankAnswer
from django.db.models.functions import Length
import numpy as np
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
from django.shortcuts import redirect

attr_num = 5
attention = 60
total = 0
complete = 0
remain = 0
min = 0
sec = 0

f = pd.DataFrame()

def sec_to_min(x):
    m = x//60
    s = x%60
    if s<30:
        return int(m)
    else:
        return int(m+1)

@csrf_exempt
def change_filter(request):
    if request.method == 'POST':
        # gives list of id of inputs
        list_of_input_ids = request.POST.getlist('inputs')

@csrf_exempt
def show_thumbnail(request):
    global attention, total, complete, remain, f, min, sec
    context = {}
    context["total"] = total
    context["complete"] = complete
    context["remain"] = remain
    context["attention"] = attention
    context["min"] = min
    context["sec"] = sec
    for i in range(2):  # article
        srcs = []
        for j in range(17):
            srcs.append({"text":"Thumbnail"+str(j+1), "src":"images\\tnv"+str(i+1)+"\\"+str(j+1)+".png"})
        context["article"+str(i+1)] = srcs
    return render(request, 'Dashboard/thumbnail.html', context)

@csrf_exempt
def stat_participant(request):
    global attention, total, complete, remain, f, min, sec
    context = {}
    context["total"] = total
    context["complete"] = complete
    context["remain"] = remain
    context["attention"] = attention
    context["min"] = min
    context["sec"] = sec
    infolist = ['time','attention','age', 'vis', 'gender', 'education', 'news']
    edu = ["High School","(University/College)","M.S", "PhD"]
    news = ["None","less than 2","less than 5","less than 7","more than 7"]
    context["user_info"] = []
   # f = pd.DataFrame(list(RankAnswer.objects.filter(isFinish=True, passTrap=True).values()))

    if remain>0:
        for info in infolist:
            df = f[info]
            df_list = list(df)
            vals = {}
            vals["text"] = info
            vals["child"] = []

            if info=="time":
                vals["stat"] = {}
                vals["stat"]["child"] = []
                vals["stat"]["child"].append({"text":"mean","child":[{"text":"min","val":int(df.mean()//60)},{"text":"sec","val":int(df.mean()%60)}] })
                vals["stat"]["child"].append({"text":"std","child":[{"text":"min","val":int(df.std()//60)},{"text":"sec", "val":int(df.std()%60)}] })
                vals["stat"]["child"].append({"text":"max","child":[{"text":"min","val":int(df.max()//60)},{"text":"sec","val":int(df.max()%60)}] })
                vals["stat"]["child"].append({"text":"min","child":[{"text":"min","val":int(df.min()//60)},{"text":"sec","val":int(df.min()%60)}] })
                new_time = list(map(lambda x: sec_to_min(x), df_list))
                category = sorted(set(new_time))
                vals["columns"] = category
                vals["child"] = []
                for c in category:
                   # vals["child"].append({"text": c, "val": new_time.count(c)})
                     vals["child"].append( new_time.count(c) )
            elif info=="age" or info=="attention" or info=="vis":
                vals["stat"] = {}
                vals["stat"]["child"] = []
                vals["stat"]["child"].append({"text":"mean","val":int(df.mean())})
                vals["stat"]["child"].append({"text":"std","val":int(df.std())})
                vals["stat"]["child"].append({"text":"max","val":int(df.max())})
                vals["stat"]["child"].append({"text":"min","val":int(df.min())})
                category = sorted(set(df))
                vals["columns"] = category
                vals["child"] = []
                for c in category:
                    #vals["child"].append({"text": c, "val": df_list.count(c)})
                    vals["child"].append( df_list.count(c) )
            else:
                if info=="education":
                    vals["columns"] = edu
                    vals["child"] = []
                    vals["stat"] = {}
                    vals["stat"]["child"] = []
                    vals["stat"]["child"].append({"text": "mean", "val": edu[int(df.mean())-1]})
                    vals["stat"]["child"].append({"text": "std", "val": int(df.std())})
                    vals["stat"]["child"].append({"text": "max", "val": edu[int(df.max())-1]})
                    vals["stat"]["child"].append({"text": "min", "val": edu[int(df.min())-1]})
                    for c in vals["columns"]:
                        #vals["child"].append({"text": c, "val": df_list.count(edu.index(c)+1)})
                        vals["child"].append(df_list.count(edu.index(c)+1))
                elif info=="news":
                    vals["columns"] = news
                    vals["child"] = []
                    vals["stat"] = {}
                    vals["stat"]["child"] = []
                    vals["stat"]["child"].append({"text": "mean", "val": news[int(df.mean())-1]})
                    vals["stat"]["child"].append({"text": "std", "val": int(df.std())})
                    vals["stat"]["child"].append({"text": "max", "val": news[int(df.max())-1]})
                    vals["stat"]["child"].append({"text": "min", "val": news[int(df.min())-1]})
                    for c in vals["columns"]:
                       # vals["child"].append({"text": c, "val": df_list.count(news.index(c)+1)})
                        vals["child"].append(df_list.count(news.index(c)+1))
                elif info=="gender":
                    category = sorted(set(df))
                    vals["columns"] = category
                    vals["child"] = []
                    for c in category:
                        # vals["child"].append({"text": c, "val": df_list.count(c)})
                        vals["child"].append(df_list.count(c))

            context['user_info'].append(vals)

        return render(request, 'Dashboard/participant.html', context)
    else:
        context["message"] = "No participants"
        return render(request, 'master.html', context)

@csrf_exempt
def stat_correlation(request):
    global attention, total, complete, remain, f, min, sec
    context = {}
    context["total"] = total
    context["complete"] = complete
    context["remain"] = remain
    context["attention"] = attention
    context["min"] = min
    context["sec"] = sec
    attr_name = ["MP", "CTX", "DA", "AEST", "OA"]

    attr_idx = 4
    if request.method == 'POST':
        attr_idx = attr_name.index(request.POST['attr'])

    context["attr"] = attr_name[attr_idx]

    if remain>0:
      #  f = pd.DataFrame(list(RankAnswer.objects.filter(isFinish=True, passTrap=True, attention__lte=int(attention)).values()))

        for i in range(2):  # article
            tnvs = {}
            tnvs["text"] = 'article' + str(i + 1)
            tnvs["child"] = []
            init = True
            global_list = []
            for j in range(17):  # tnv
                local_list = []
                corr = {}
                corr["text"] = 'tnv' + str(j + 1)
                corr["child"] = []

                if init:
                    for k in range(attr_num):
                        local_list.append(list(f['a' + str(i + 1) + 'g' + str(k + 1) + 't' + str(j + 1)]))
                        #global_list.append(local_list[k])
                        global_list.append([np.mean(local_list[k])])
                    init = False
                else:
                    for k in range(attr_num):
                        local_list.append(list(f['a' + str(i + 1) + 'g' + str(k + 1) + 't' + str(j + 1)]))
                        #global_list[k] = map(lambda x,y : x+y, global_list[k], local_list[k])
                        global_list[k].append(np.mean(local_list[k]))

                for m in range(attr_num):
                    if m != attr_idx:
                        val = list(scipy.stats.pearsonr(local_list[m], local_list[attr_idx]))
                        attr = {}
                        attr["text"] = attr_name[m]
                        attr["child"] = []
                        attr["child"].append({"text": "r", "val": round(val[0], 4)})
                        if round(val[1], 4) == 0:
                            attr["child"].append({"text": "p", "val": "<0.0001"})
                        else:
                            attr["child"].append({"text": "p", "val": round(val[1], 4)})
                        corr["child"].append(attr)

                tnvs["child"].append(corr)

            #for m in range(attr_num):
            #    global_list[m] = [x / 17 for x in global_list[m]]

            corr = {}
            corr["text"] = "total"
            corr["child"] = []

            for m in range(attr_num):
                if m != attr_idx:
                    val = list(scipy.stats.pearsonr(global_list[m], global_list[attr_idx]))
                    attr = {}
                    attr["text"] = attr_name[m]
                    attr["child"] = []
                    attr["child"].append({"text": "r", "val": round(val[0], 4)})
                    if round(val[1], 4) == 0:
                        attr["child"].append({"text": "p", "val": "<0.0001"})
                    else:
                        attr["child"].append({"text": "p", "val": round(val[1], 4)})
                    corr["child"].append(attr)

            tnvs["child"].append(corr)

            context["article"+str(i+1)] = tnvs
        return render(request, 'Dashboard/correlation.html', context)
    else:
        context["message"] = "No participants"
        return render(request, 'master.html', context)

@csrf_exempt
def stat_anova(request):
    global attention, total, complete, remain, f, min, sec
    context = {}
    context["total"] = total
    context["complete"] = complete
    context["remain"] = remain
    context["attention"] = attention
    context["min"] = min
    context["sec"] = sec
    attr_name = ["MP", "CTX", "DA", "AEST", "OA"]

    tnv_list = []
    for i in range(17):
        tnv_list.append("Tn"+str(i+1))

    if remain>0:
       # f = pd.DataFrame(list(RankAnswer.objects.filter(isFinish=True, passTrap=True, attention__lte=int(attention)).values()))
        for i in range(2):  # article
            attr_list = [[], [], [], [], []]
            mean_list = [[], [], [], [], []]
            std_list = [[], [], [], [], []]

            attrs = {}
            attrs["text"] = 'article' + str(i + 1)
            attrs["columns"] = tnv_list
            attrs["child"] = []

            for j in range(17):  # tnv
                for k in range(attr_num):
                    attr_list[k].append(f['a' + str(i + 1) + 'g'+ str(k+1) + 't' + str(j + 1)])
                    mean_list[k].append(round(f['a' + str(i + 1) + 'g'+ str(k+1) + 't' + str(j + 1)].mean(),2))
                    std_list[k].append(round(f['a' + str(i + 1) + 'g'+ str(k+1) + 't' + str(j + 1)].std(),2))

            for q in range(attr_num):
                vals = {}
                vals["text"] = attr_name[q]
                vals["child"] = {}
                vals["child"]["mean"] = mean_list[q]
                vals["child"]["std"] = std_list[q]

                vals["child"]["anova"] = []
                fVal, pVal = scipy.stats.f_oneway(*[l for l in attr_list[q]])
                vals["child"]["anova"].append({"text":"fVal", "val":fVal})
                vals["child"]["anova"].append({"text":"pVal", "val":pVal})
                attrs["child"].append(vals)

            context["article"+str(i+1)] = attrs
        return render(request, 'Dashboard/anova.html', context)
    else:
        context["message"] = "No participants"
        return render(request, 'master.html', context)

@csrf_exempt
def stat_result(request):
    global attention, total, complete, remain, f, min, sec
    context = {}
    context["total"] = total
    context["complete"] = complete
    context["remain"] = remain
    context["attention"] = attention
    context["min"] = min
    context["sec"] = sec
    attr_name = ["MP", "CTX", "DA", "AEST", "OA"]
    if remain>0:
       # f = pd.DataFrame(list(RankAnswer.objects.filter(isFinish=True, passTrap=True, attention__lte=int(attention)).values()))

        for i in range(2):  # article
            total_max = [0, 0, 0, 0, 0]
            total_min = [0, 0, 0, 0, 0]
            total_mean = [0, 0, 0, 0, 0]
            total_std = [0, 0, 0, 0, 0]
            tnvs = {}
            tnvs["text"] = 'article' + str(i + 1)
            tnvs["child"] = []
            for j in range(17):  # tnv
                vals = {}
                vals["text"] = 'tnv'+str(j+1)
                vals["child"] = []
                for q in range(attr_num):
                    val = {}
                    val["text"] = attr_name[q]
                    val["child"] = []
                    val["child"].append({"text":'max', "val":f['a' + str(i + 1) + 'g'+ str(q+1) + 't' + str(j + 1)].max()})
                    val["child"].append({"text":'min', "val":f['a' + str(i + 1) + 'g'+ str(q+1) + 't' + str(j + 1)].min()})
                    val["child"].append({"text":'mean', "val":round(f['a' + str(i + 1) + 'g'+ str(q+1) + 't' + str(j + 1)].mean(), 2)})
                    val["child"].append({"text":'std', "val":round(f['a' + str(i + 1) + 'g'+ str(q+1) + 't' + str(j + 1)].std(), 2)})
                    vals["child"].append(val)

                    total_max[q] += val['child'][0]['val']
                    total_min[q] += val['child'][1]['val']
                    total_mean[q] += val['child'][2]['val']
                    total_std[q] += val['child'][3]['val']

                tnvs["child"].append(vals)

            vals = {}
            vals["text"] = 'total'
            vals["child"] = []
            for k in range(attr_num):
                val = {}
                val["text"] = attr_name[k]
                val["child"] = []
                val["child"].append({"text": 'max', "val": round(total_max[k]/17, 2)})
                val["child"].append({"text": 'min', "val": round(total_min[k]/17, 2)})
                val["child"].append({"text": 'mean', "val": round(total_mean[k]/17, 2)})
                val["child"].append({"text": 'std', "val": round(total_std[k]/17, 2)})
                vals["child"].append(val)
            tnvs["child"].append(vals)
            context["article"+str(i+1)] = tnvs
        return render(request, 'Dashboard/result.html', context)
    else:
        context["message"] = "No participants"

        return render(request, 'master.html', context)

def upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'Dashboard/upload.html', {
            'uploaded_file_url': uploaded_file_url
        })

    return render(request, 'Dashboard/upload.html')

@csrf_exempt
def change_attention(request):
    global attention, total, complete, passTrap, remain, f, min, sec
    context = {}
    context["total"] = total
    context["complete"] = complete
    context["remain"] = remain
    context["attention"] = attention

    # 0:all, 1:trap check, 2:attention check, 3:tran & attention check
    filter_case = 0
    if request.method == 'POST':
        attention = request.POST['attention-val']
        current_url = request.POST['current-url']
     #   if 'trap-check' in request.POST:
     #       filter_case = 1
        if 'attention-check' in request.POST:
            if filter_case == 0:
                filter_case = 2
            else:
                filter_case = 3

        if filter_case == 0:
            f = pd.DataFrame(list(RankAnswer.objects.filter(isFinish=True).values()))
            remain = RankAnswer.objects.filter(isFinish=True).count()
        elif filter_case == 1:
            f = pd.DataFrame(list(RankAnswer.objects.filter(isFinish=True, passTrap=True).values()))
            remain = RankAnswer.objects.filter(isFinish=True, passTrap=True).count()
        elif filter_case == 2:
            f = pd.DataFrame(list(RankAnswer.objects.filter(isFinish=True, attention__lte=int(attention)).values()))
            remain = RankAnswer.objects.filter(isFinish=True, attention__lte=int(attention)).count()
        elif filter_case == 3:
            f = pd.DataFrame(list(RankAnswer.objects.filter(isFinish=True, passTrap=True, attention__lte=int(attention)).values()))
            remain = RankAnswer.objects.filter(isFinish=True, passTrap=True, attention__lte=int(attention)).count()

        context["remain"] = remain
        context["attention"] = attention
        context["min"] = min
        context["sec"] = sec
        return redirect(current_url)
    return render(request, 'master.html', context)

def main(request):
    global attention, total, complete, passTrap, remain, f, min, sec
    total = RankAnswer.objects.filter().count()
    complete = RankAnswer.objects.filter(isFinish=True).count()
    remain = RankAnswer.objects.filter(isFinish=True).count()
    f = pd.DataFrame(list(RankAnswer.objects.filter(isFinish=True).values()))
    context = {}
    if len(f) != 0:
        df = f["time"]
        min = int(df.mean() // 60)
        sec = int(df.mean() % 60)
        context["total"] = total
        context["complete"] = complete
        context["remain"] = remain
        context["attention"] = attention
        context["min"] = min
        context["sec"] = sec
    return render(request, 'master.html',  context)
