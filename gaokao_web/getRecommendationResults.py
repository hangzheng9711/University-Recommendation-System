from .models import trainingSet
from .models import yiFenYiDang
from .models import line
from.xietongguolv import UserCf

class RecRes():

    #获得初始化数据
    def __init__(self, data):#{'score':640, 'place':"重庆", 'subject':"理科"}
        self.data=data;

    def getRank(self):
        minScoreLine = yiFenYiDang.objects.filter(place=self.data['place'], subject=self.data['subject']).order_by('score')[0]
        minScore = minScoreLine.score
        minRank = minScoreLine.rank
        maxScoreLine = yiFenYiDang.objects.filter(place=self.data['place'], subject=self.data['subject']).order_by('-score')[0]
        maxScore = maxScoreLine.score
        maxRank = maxScoreLine.rank
        if(self.data['score']>maxScore):
            rank=maxRank
        elif(self.data['score']<minScore):
            rank=minRank
        else:
            dataForRank = yiFenYiDang.objects.get(score=self.data['score'], place=self.data['place'], subject=self.data['subject'])
            rank = dataForRank.rank
        return rank

    def getGapLayer(self):
        dataForGapLayer = line.objects.get(place=self.data['place'], subject=self.data['subject'])
        if self.data['score'] >= dataForGapLayer.line1:
            gapLayer = 1
        elif self.data['score'] >= dataForGapLayer.line2:
            gapLayer = 2
        else:
            gapLayer = 3
        return gapLayer

    def getGap(self):
        dataForGap = line.objects.get(place=self.data['place'], subject=self.data['subject'])
        if self.data['score'] >= dataForGap.line1:
            gap = self.data['score'] - dataForGap.line1
        elif self.data['score'] >= dataForGap.line2:
            gap = self.data['score'] - dataForGap.line2
        else:
            gap = self.data['score'] - dataForGap.line3
        return gap

    def getKeyAndValue(self):
        dataforLine = line.objects.get(place=self.data['place'], subject=self.data['subject'])
        if self.data['score']>=dataforLine.line1+100:
            dangci=5
            key=1
            value=50
        elif self.data['score']<dataforLine.line1+100 and self.data['score']>=dataforLine.line1:
            dangci=4
            key=1
            value=150
        elif self.data['score']<dataforLine.line1 and self.data['score']>=dataforLine.line2:
            dangci=3
            key=1
            value=250
        elif self.data['score']<dataforLine.line2 and self.data['score']>=dataforLine.line3:
            dangci=2
            key=0
            value=0.85
        else:
            dangci=1
            key=0
            value=0.8
        return dangci,key,value

    def getRecLis(self):
        if self.data['line'] == '0':
            data = trainingSet.objects.filter(place=self.data['place'], subject=self.data['subject'], major__contains=self.data['major'])
        else:
            data = trainingSet.objects.filter(place=self.data['place'], subject=self.data['subject'], major__contains=self.data['major'], line=self.data['line'])
        if self.data['city'] != '0':
            data = data.filter(city=self.data['city'])
        gapLayer = self.getGapLayer()
        allTrainingData = []

        for i in data:
                trainingData = {}
                trainingData['school'] = i.school
                trainingData['major'] = i.major
                trainingData['line'] = i.line
                trainingData['score'] = i.score
                trainingData['rank'] = i.rank
                if gapLayer == 1:
                    trainingData['gap'] = i.gap1
                elif gapLayer == 2:
                    trainingData['gap'] = i.gap2
                else:
                    trainingData['gap'] = i.gap3
                allTrainingData.append(trainingData)

        dangci,key,value=self.getKeyAndValue()

        userCf = UserCf(data=allTrainingData)
        recommandList=userCf.recommand({'score': self.data['score'], 'rank': self.getRank(), 'gap': self.getGap()},key,value)
        return recommandList

    def getRecLisFinal(self, recommandList):
        #重新计算录取概率
        for key, value in dict(recommandList).items():
            length = len(value['录取概率'])
            for i in range(1, length + 1):
                value['录取概率'][i - 1] = str(round(value['录取概率'][i - 1] * 100, 2)) + '%'

        #将字典变为列表
        recommendListFinal=[]
        for key, value in recommandList.items():
            dictEvery={}
            dictEvery['学校'] = key
            dictEvery['批次'] = value['批次']
            dictEvery['专业列表'] = value['专业列表']
            dictEvery['录取概率'] = value['录取概率']
            recommendListFinal.append(dictEvery)

        return recommendListFinal