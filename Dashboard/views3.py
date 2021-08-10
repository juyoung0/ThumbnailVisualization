from django.shortcuts import render
import json, os, csv
import pandas as pd
import numpy as np
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import scipy.stats
from Turk.models import ScoreAnswer
from Dashboard.descriptions import des1, des2
from django.db.models.functions import Length
import numpy as np
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
from django.shortcuts import redirect

total = 0
complete = 0
min = 0
sec = 0
f = pd.DataFrame()

questions = {"q1":"1. This description effectively summarizes the context of the article.",
        "q2":"2. This thumbnail and the description are matching well.",
        "q3":"3. This thumbnail and the description effectively represent the article. "}

def sec_to_min(x):
    m = x//60
    s = x%60
    if s<30:
        return int(m)
    else:
        return int(m+1)

@csrf_exempt
def show_thumbnail(request):
    global total, complete, f, min, sec
    context = {}
    context["total"] = total
    context["complete"] = complete
    context["min"] = min
    context["sec"] = sec

    for i in range(2):  # article
        srcs = []
        for j in range(17):
            srcs.append({"text":"Thumbnail"+str(j+1), "src":"images\\tnv"+str(i+1)+"\\"+str(j+1)+".png"})
        context["article"+str(i+1)] = srcs
    return render(request, 'Dashboard/thumbnail3.html', context)

@csrf_exempt
def show_tn(request):
    global total, complete, f, min, sec
    context = {}
    context["total"] = total
    context["complete"] = complete
    context["min"] = min
    context["sec"] = sec
    tn_num = int(request.GET['tn_num'])
    df = pd.DataFrame(list(ScoreAnswer.objects.filter(isFinish=True, tn=tn_num).values()))
    des_num = 5
    question_num = 3
    scale = 7

    if not df.empty :
        context["tn"] = {}
        context["tn"]["title"] = "Thumbnail" + str(tn_num)

        context["tn"]["child"] = []
        context["tn"]["columns"] = ["1","2","3","4","5","6","7"]
        df_temp = df.loc[df.tn == tn_num]
        context["tn"]["people"] = len(df_temp.index)
        print(df_temp.head())

        for des in range(des_num):
            desDict = {}

            if des==1:
                desDict["description"] = des1
            else:
                desDict["description"] = des2

            desDict["table"] = []
            desDict["child"] = []

            for q in range(question_num):
                vals = {}
                vals["text"] = questions["q"+str(q+1)]
                vals["child"] = []
                desDict["table"].append({"text":"q"+str(q+1), "mean": df_temp["d"+ str(des+1) +"q"+ str(q + 1)].mean(), "std": round(df_temp["d"+ str(des+1) + "q" + str(q + 1)].std(),2) })

                for s in range(scale):
                    vals["child"].append(len(df_temp.loc[df_temp["d"+ str(des+1) +"q"+str(q+1)] == s+1]))

                desDict["child"].append(vals)

            context["tn"]["child"].append(desDict)

        return render(request, 'Dashboard/study4tn.html', context)
    else:
        context["message"] = "No participants"
        return render(request, 'master3.html', context)
@csrf_exempt
def stat_participant(request):
    global total, complete, f, min, sec
    context = {}
    context["total"] = total
    context["complete"] = complete
    context["min"] = min
    context["sec"] = sec
    infolist = ['time','age', 'vis', 'gender', 'education', 'news']
    edu = ["High School","(University/College)","M.S", "PhD"]
    news = ["None","less than 2","less than 5","less than 7","more than 7"]
    context["user_info"] = []
   # f = pd.DataFrame(list(RankAnswer.objects.filter(isFinish=True, passTrap=True).values()))

    if complete>0:
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

        return render(request, 'Dashboard/participant3.html', context)
    else:
        context["message"] = "No participants"
        return render(request, 'master3.html', context)


def main(request):
    global attention, total, complete, f, min, sec
    total = ScoreAnswer.objects.filter().count()
    complete = ScoreAnswer.objects.filter(isFinish=True).count()
    f = pd.DataFrame(list(ScoreAnswer.objects.filter(isFinish=True).values()))
    df = f["time"]
    min = int(df.mean() // 60)
    sec = int(df.mean() % 60)
    context = {}
    context["total"] = total
    context["complete"] = complete

    context["min"] = min
    context["sec"] = sec
    return render(request, 'master3.html',  context)
