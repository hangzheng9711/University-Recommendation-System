from django.shortcuts import render

from django.http import HttpResponse
# return HttpResponse()

from .forms import collectDataForm

from .getRecommendationResults import RecRes
from .paixu import PaiXu
from .getFCMresults import FCM

#评估
from .testPrecisionAndRecall import PreAndRec


def recommend(request):
    if request.method == 'POST':  # 提交表单

        form = collectDataForm(request.POST)  # form 包含提交的数据

        if form.is_valid() and form.is_valid():  # 如果提交的数据合法
            waypaixu = form.cleaned_data['waypaixu']

            dicData = {}
            dicData['score'] = form.cleaned_data['score']
            dicData['place'] = form.cleaned_data['place']
            dicData['subject'] = form.cleaned_data['subject']

            dicData['line'] = form.cleaned_data['line']
            dicData['major'] = form.cleaned_data['major']
            dicData['city'] = form.cleaned_data['city']

            recRes = RecRes(data=dicData)
            recDict = recRes.getRecLisFinal(recRes.getRecLis())
            dangci,key,value=recRes.getKeyAndValue()
            paiXu = PaiXu(data=recDict)
            recDictFinal = paiXu.getPaiMingandPaixu(waypaixu)
            if len(recDict)>=4:
                fcm=FCM(data=recDict)
                clusterResult = fcm.getFinalResultofCluster(dangci)
                #fcm.xie_beni(dangci,len(recDict))
            else:
                clusterResult =[]

            # 评估
            #preAndRec = PreAndRec(data=dicData)
            #preAndRec.mainPro()

    else:  # 正常访问
        form = collectDataForm(request.POST)  # form 包含提交的数据
        recDictFinal =[]
        clusterResult=[]

    return render(request, 'recommend.html', {'form': form, 'recDictFinal':recDictFinal,'clusterResult':clusterResult})