from django.shortcuts import render
import json, os, csv
import pandas as pd
import numpy as np
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import scipy.stats
from Turk.models import PredictAnswer
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
    return render(request, 'Dashboard/thumbnail2.html', context)

@csrf_exempt
def show_tn(request):
    global total, complete, f, min, sec
    context = {}
    context["total"] = total
    context["complete"] = complete
    context["min"] = min
    context["sec"] = sec
    context["description"] = {}
    context["description"]["columns"] = ['id','des','q7','q1','q2','q3','q4','q5','q6']
    context["description"]["child"] = []
    context["help"] = {}

    question_list =[ {"number":"q1", "question":"1. Describe how the thumbnail helped you to predict news article contents?"},
                     {"number":"q2", "question":"2. What are the weaknesses of the thumbnail design? "},
                   {"number":"q3", "question":"3. How could the design of the thumbnail be improved?"},
                {"number":"q4", "question":"4. Considering the news article, what important information did you miss or incorrectly describe in your prediction?"},
            {"number":"q5", "question":"5. If your prediction was incorrect or missed information, what factors contributed to these errors?"},
            {"number":"q6", "question":"6. How would you edit or augment your initial prediction based on the news article’ contents to produce a better description of the article?"},
            {"number":"q7", "question":"7. Improve your initial prediction to provide a better description of the article."}]

    context['questions'] = question_list

    tn_num = int(request.GET['tn_num'])
    df = pd.DataFrame(list(PredictAnswer.objects.filter(isFinish=True, tn=tn_num).values()))
    context['title'] = {}
    context['title']['text'] = 'Thumbnail' + str(tn_num)
    context["people"] = 0

    if not df.empty :
        data = {}
        print(df.columns)
        data['child'] = df[['id','des','q1','q7','q2','q3','q4','q5','q6']].to_dict('records')
        context["description"]["child"].append(data)
        cnt_list1 = []
        cnt_list2 = []
        cnt_list3 = []
        for i in range(7):
            cnt_list1.append(df.loc[df['help1']==i+1]['help1'].count())
            cnt_list2.append(df.loc[df['help2']==i+1]['help2'].count())
            cnt_list3.append(df.loc[df['help3']==i+1]['help3'].count())
        context["people"] = len(df.index)
        context["help"]["prev"] = { "text":"Before", "child": cnt_list1 }
        context["help"]["post"] = { "text":"After", "child": cnt_list2 }
        context["help"]["finish"] = { "text":"Finish", "child": cnt_list3 }
        context["help"]["table"] = []
        context["help"]["table"].append({ "text":"Before read article", "mean": round(df['help1'].mean(),2), "std":round(df['help1'].std(),2) })
        context["help"]["table"].append({ "text":"After read article", "mean": round(df['help2'].mean(),2), "std":round(df['help2'].std(),2) })
        context["help"]["table"].append({ "text":"After whole task", "mean": round(df['help3'].mean(),2), "std":round(df['help3'].std(),2) })

    else:
        context["message"] = "No participants"

    return render(request, 'Dashboard/study3tn.html', context)

@csrf_exempt
def show_artilce2(request):
    global total, complete,f, min, sec
    context = {}
    context["total"] = total
    context["complete"] = complete
    context["min"] = min
    context["sec"] = sec
    context["article2"] = {}
    context["article2"]["columns"] = ['des', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6']
    context["article2"]["child"] = []

    if complete > 0 :
        for j in range(4):
            data = {}
            data['text'] = 'Thumbnail'+str(j+1)
            data['src'] = "images\\tnv2"+"\\"+str(j+1)+".png"
            df = f.loc[f['tn']==j+5]
            data['child'] = df[['des', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6']].to_dict('records')
            context["article2"]["child"].append(data)
    else:
        context["message"] = "No participants"
    return render(request, 'Dashboard/study3article2.html', context)

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

        return render(request, 'Dashboard/participant2.html', context)
    else:
        context["message"] = "No participants"
        return render(request, 'master2.html', context)


def main(request):
    global total, complete, passTrap, f, min, sec
    total = PredictAnswer.objects.filter().count()
    complete = PredictAnswer.objects.filter(isFinish=True).count()
    f = pd.DataFrame(list(PredictAnswer.objects.filter(isFinish=True).values()))
    context = {}
    if len(f) != 0:
        df = f["time"]
        min = int(df.mean() // 60)
        sec = int(df.mean() % 60)
        context["total"] = total
        context["complete"] = complete
        context["min"] = min
        context["sec"] = sec
    return render(request, 'master2.html',  context)
