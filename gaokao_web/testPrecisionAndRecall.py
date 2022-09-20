from .models import testXieTongGuoLv
from.getRecommendationResults import RecRes

import matplotlib.pyplot as plt

class PreAndRec():

    #获得初始化数据
    def __init__(self, data):#{'score':640, 'place':"重庆", 'subject':"理科"}
        self.data=data;

    def getSchoolList(self):
        recRes = RecRes(data=self.data)
        recDict = recRes.getRecLis()
        schoolList = []
        for key in recDict:
            schoolList.append(key)
        return schoolList

    def getScoreList(self,schoolList):
        scoreList = []
        for i in schoolList:
            scoreList.append(testXieTongGuoLv.objects.get(place=self.data['place'],subject=self.data['subject'],school=i).score)
        return scoreList

    def calXandH(self,scoreList):
        numberx=0
        numberh=0
        for i in scoreList:
            if self.data['score']-i>=0 and self.data['score']-i<=10:
                numberx=numberx+1
            numberh=numberh+1
        return numberx,numberh

    def calY(self):
        data = testXieTongGuoLv.objects.filter(place=self.data['place'],subject=self.data['subject'],score__gte=self.data['score']-10,score__lte=self.data['score'])
        #__gte 大于等于 __lte 小于等于
        return len(data)

    def mainPro(self):
        schoolList = self.getSchoolList()
        scoreList = self.getScoreList(schoolList)
        x,h = self.calXandH(scoreList)
        y = self.calY()
        if h == 0:
            precision=0
        else:
            precision=float(x/h)
        if y == 0:
            recall=0
        else:
            recall=float(x/y)
        print(precision)
        print(recall)
        return precision,recall
        #precisionResultList=[]
        #recallResultList=[]
        #numberList=[5,15,25,35,45,55,65,75,85,95,105,115,125,135,145,155,165,175,185,195,205,215,225,235,245,255,265,275,285,295]
        #for i in numberList:
        #    schoolList = self.getSchoolList(i)
        #    scoreList = self.getScoreList(schoolList)
        #    x,h = self.calXandH(scoreList)
        #    y = self.calY()
        #    if h == 0:
        #        precisionResultList.append(0)
        #    else:
        #       precisionResultList.append(float(x/h))
        #    if y == 0:
        #        recallResultList.append(0)
        #    else:
        #        recallResultList.append(float(x/y))
        #print(numberList)
        #print(precisionResultList)
        #print(recallResultList)
        #print(max(precisionResultList))
        #print(precisionResultList.index(max(precisionResultList)))
        #print(max(recallResultList))
        #print(recallResultList.index(max(recallResultList)))

        #plt.figure()
        #plt.plot(numberList, precisionResultList, color='blue', label='precision')
        #plt.plot(numberList, recallResultList, color='yellow', label='recall')
        #plt.legend()  # 显示图例
        #plt.xlabel("number")  # X轴标签
        #plt.ylabel("rate")  # Y轴标签
        #plt.title("Precision and Recall")  # 图标题
        #plt.show()  # 显示图

        #return precisionResultList,recallResultList

#    {'四川大学': {'批次': '本科第一批', '专业列表': ['计算机科学与技术', '临床医学'],
#    '录取概率': [0.999999995715267, 0.9593742892916977]},
#    '北京理工大学': {'批次': '本科第一批', '专业列表': ['物理'],
#    '录取概率': [0.9999907659707307]},
#    '南开大学': {'批次': '本科第一批', '专业列表': ['电子信息'], '录取概率': [0.9174279214505371]}}