from django.shortcuts import render
import json, os, csv
import pandas as pd
import numpy as np
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import scipy.stats
from Turk.models import CompareAnswer
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
def stat_result(request):
    global total, complete, f, min, sec
    tn_type = request.GET['tn_type']
    context = {}
    context["total"] = total
    context["complete"] = complete
    context["min"] = min
    context["sec"] = sec
    context["questions"] = {}
    context["ans"] = {}

    df = pd.DataFrame(list(CompareAnswer.objects.filter(isFinish=True).values()))

    if tn_type=="a":
        question_list =[ {"number":"q0","question":"id"},
                         {"number":"q1", "question":"Why would you choose (A)?"},
                         {"number": "q2", "question": "Why not (B)?"},
                         {"number": "q3", "question": "Why not (C)?"},
                         {"number": "q4", "question": "Why not (D)?"}]
    elif tn_type=="b":
        question_list =[ {"number":"q0","question":"id"},
                         {"number":"q1", "question":"Why would you choose (B)?"},
                         {"number": "q2", "question": "Why not (A)?"},
                         {"number": "q3", "question": "Why not (C)?"},
                         {"number": "q4", "question": "Why not (D)?"}]
    elif tn_type == "c":
            question_list = [{"number":"q0","question":"id"},
                             {"number": "q1", "question": "Why would you choose (C)?"},
                             {"number": "q2", "question": "Why not (A)?"},
                             {"number": "q3", "question": "Why not (B)?"},
                             {"number": "q4", "question": "Why not (D)?"}]
    elif tn_type == "d":
        question_list = [{"number":"q0","question":"id"},
                         {"number": "q1", "question": "Why would you choose (D)?"},
                         {"number": "q2", "question": "Why not (A)?"},
                         {"number": "q3", "question": "Why not (B)?"},
                         {"number": "q4", "question": "Why not (C)?"}]

    context['questions'] = question_list

    if not df.empty :
        cnt_list = []
        anova_list = []
        num = len(df.loc[df['q1'] == 'A'].index)
        cnt_list.append(num)
        anova_df1 = pd.DataFrame({'A': np.ones(num), 'B': np.zeros(num), 'C': np.zeros(num), 'D': np.zeros(num)})
        num = len(df.loc[df['q1'] == 'B'].index)
        cnt_list.append(num)
        anova_df2 = pd.DataFrame({'A': np.zeros(num), 'B': np.ones(num), 'C': np.zeros(num), 'D': np.zeros(num)})
        num = len(df.loc[df['q1'] == 'C'].index)
        cnt_list.append(num)
        anova_df3 = pd.DataFrame({'A': np.zeros(num), 'B': np.zeros(num), 'C': np.ones(num), 'D': np.zeros(num)})
        num = len(df.loc[df['q1'] == 'D'].index)
        cnt_list.append(num)
        anova_df4 = pd.DataFrame({'A': np.zeros(num), 'B': np.zeros(num), 'C': np.ones(num), 'D': np.zeros(num)})
        context["ans"]["cnt"] = cnt_list

        #카이검정
        #cnt_real = [elem/complete for elem in cnt_list]
        #print(cnt_list)
        #print(cnt_real)
        cnt_expect = [complete/4, complete/4, complete/4, complete/4]
        chis = scipy.stats.chisquare(cnt_list, cnt_expect)
        context["ans"]["chi"] = []
        context["ans"]["chi"].append({"text": "statistic", "val": round(chis.statistic,4)})
        context["ans"]["chi"].append({"text": "pVal", "val": round(chis.pvalue,4)})

        frames = [anova_df1, anova_df2, anova_df3, anova_df4]
        anova_df = pd.concat(frames, ignore_index=True)
        anova_list.append(anova_df['A'].tolist())
        anova_list.append(anova_df['B'].tolist())
        anova_list.append(anova_df['C'].tolist())
        anova_list.append(anova_df['D'].tolist())

        context["ans"]["anova"] = []
        fVal, pVal = scipy.stats.f_oneway(*[l for l in anova_list])
        context["ans"]["anova"].append({"text": "fVal", "val": round(fVal,4)})
        context["ans"]["anova"].append({"text": "pVal", "val": round(pVal,4)})

        if tn_type=='a':
            context["ans"]["title"] = "Thumbnail A"
            temp_df = df.loc[df['q1'] == 'A']
            context["ans"]["des"] = temp_df[['id','q2','q3b','q3c','q3d']].rename(columns = {'q2':'q1', 'q3b':'q2','q3c':'q3','q3d':'q4'}).to_dict('records')
        elif tn_type=='b':
            context["ans"]["title"] = "Thumbnail B"
            temp_df = df.loc[df['q1'] == 'B']
            context["ans"]["des"] = temp_df[['id','q2','q3a','q3c','q3d']].rename(columns = {'q2':'q1', 'q3a':'q2','q3c':'q3','q3d':'q4'}).to_dict('records')
        elif tn_type=='c':
            context["ans"]["title"] = "Thumbnail C"
            temp_df = df.loc[df['q1'] == 'C']
            context["ans"]["des"] = temp_df[['id','q2','q3a','q3b','q3d']].rename(columns = {'q2':'q1', 'q3a':'q2','q3b':'q3','q3d':'q4'}).to_dict('records')
        elif tn_type=='d':
            context["ans"]["title"] = "Thumbnail D"
            temp_df = df.loc[df['q1'] == 'D']
            context["ans"]["des"] = temp_df[['id','q2','q3a','q3b','q3c']].rename(columns = {'q2':'q1', 'q3a':'q2','q3b':'q3','q3c':'q4'}).to_dict('records')
    else:
        context["message"] = "No participants"

    return render(request, 'Dashboard/compareResult.html', context)


@csrf_exempt
def question(request):
    global total, complete, f, min, sec
    context = {}
    context["total"] = total
    context["complete"] = complete
    context["min"] = min
    context["sec"] = sec

    df = pd.DataFrame(list(CompareAnswer.objects.filter(isFinish=True).values()))

    if not df.empty :
        context["ans"] = df[['id','q3']].to_dict('records')
        context['question'] = {"text":"What do you want to “see” from thumbnails?"}
    else:
        context["message"] = "No participants"

    return render(request, 'Dashboard/question.html', context)

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

        return render(request, 'Dashboard/participant4.html', context)
    else:
        context["message"] = "No participants"
        return render(request, 'master4.html', context)


def main(request):
    global attention, total, complete, f, min, sec
    total = CompareAnswer.objects.filter().count()
    complete = CompareAnswer.objects.filter(isFinish=True).count()
    f = pd.DataFrame(list(CompareAnswer.objects.filter(isFinish=True).values()))
    context = {}
    if len(f) != 0:
        df = f["time"]
        min = int(df.mean() // 60)
        sec = int(df.mean() % 60)
        context["total"] = total
        context["complete"] = complete
        context["min"] = min
        context["sec"] = sec
    return render(request, 'master4.html',  context)
