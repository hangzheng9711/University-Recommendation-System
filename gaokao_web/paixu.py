'''
排序
'''

from .models import school

class PaiXu():

    #获得初始化数据
    def __init__(self,data):
        self.data=data;

    def getPaiMingandPaixu(self,s):
        recommendList=[]
        length = len(self.data)
        if s=='0' or s=='1':
            for i in range(0,length):
                dictEvery = {}
                dictEvery['学校'] = self.data[i]['学校']
                dictEvery['批次'] = self.data[i]['批次']
                dictEvery['专业列表'] = self.data[i]['专业列表']
                dictEvery['录取概率'] = self.data[i]['录取概率']
                meaningschool = school.objects.get(name=dictEvery['学校'])
                dictEvery['排名'] = int((meaningschool.scorewd1+meaningschool.scorewd2+meaningschool.scorewsl1+ meaningschool.scorewsl2+meaningschool.scorexyh+meaningschool.employment+meaningschool.esipaper+meaningschool.esisubject)/8*100)
                recommendList.append(dictEvery)
            if s=='1':
                recommendListLast=sorted(recommendList, key=lambda recommendList: recommendList['排名'], reverse=True)
            else:
                recommendListLast=recommendList;
        elif s=='scorexyh':
            for i in range(0,length):
                dictEvery = {}
                dictEvery['学校'] = self.data[i]['学校']
                dictEvery['批次'] = self.data[i]['批次']
                dictEvery['专业列表'] = self.data[i]['专业列表']
                dictEvery['录取概率'] = self.data[i]['录取概率']
                meaningschool = school.objects.get(name=dictEvery['学校'])
                dictEvery['排名'] = int(meaningschool.scorexyh*100)
                recommendList.append(dictEvery)
            recommendListLast=sorted(recommendList, key=lambda recommendList: recommendList['排名'], reverse=True)
        elif s == 'scorewsl':
            for i in range(0,length):
                dictEvery = {}
                dictEvery['学校'] = self.data[i]['学校']
                dictEvery['批次'] = self.data[i]['批次']
                dictEvery['专业列表'] = self.data[i]['专业列表']
                dictEvery['录取概率'] = self.data[i]['录取概率']
                meaningschool = school.objects.get(name=dictEvery['学校'])
                dictEvery['排名'] = int((meaningschool.scorewsl1+meaningschool.scorewsl2)/2 * 100)
                recommendList.append(dictEvery)
            recommendListLast=sorted(recommendList, key=lambda recommendList: recommendList['排名'], reverse=True)
        elif s=='scorewd':
            for i in range(0,length):
                dictEvery = {}
                dictEvery['学校'] = self.data[i]['学校']
                dictEvery['批次'] = self.data[i]['批次']
                dictEvery['专业列表'] = self.data[i]['专业列表']
                dictEvery['录取概率'] = self.data[i]['录取概率']
                meaningschool = school.objects.get(name=dictEvery['学校'])
                dictEvery['排名'] = int((meaningschool.scorewd1+meaningschool.scorewd2)/2 * 100)
                recommendList.append(dictEvery)
            recommendListLast=sorted(recommendList, key=lambda recommendList: recommendList['排名'], reverse=True)
        elif s=='esi':
            for i in range(0,length):
                dictEvery = {}
                dictEvery['学校'] = self.data[i]['学校']
                dictEvery['批次'] = self.data[i]['批次']
                dictEvery['专业列表'] = self.data[i]['专业列表']
                dictEvery['录取概率'] = self.data[i]['录取概率']
                meaningschool = school.objects.get(name=dictEvery['学校'])
                dictEvery['排名'] = int((meaningschool.esisubject+meaningschool.esipaper)/2 * 100)
                recommendList.append(dictEvery)
            recommendListLast=sorted(recommendList, key=lambda recommendList: recommendList['排名'], reverse=True)
        elif s == 'emp':
            for i in range(0, length):
                dictEvery = {}
                dictEvery['学校'] = self.data[i]['学校']
                dictEvery['批次'] = self.data[i]['批次']
                dictEvery['专业列表'] = self.data[i]['专业列表']
                dictEvery['录取概率'] = self.data[i]['录取概率']
                meaningschool = school.objects.get(name=dictEvery['学校'])
                dictEvery['排名'] = int(meaningschool.employment*100)
                recommendList.append(dictEvery)
            recommendListLast = sorted(recommendList, key=lambda recommendList: recommendList['排名'], reverse=True)
        return recommendListLast

#    recommendList = {北京理工大学:{'批次': '本科第一批',
#                                 '专业列表': ['电子科学与技术', '计算机类', '自动化', '光电信息科学与工程', '计算机科学与技术', '兵器类', '机械类', '机械电子工程', '材料科学与工程', '自动化类', '航空航天类', '化工与制药类'],
#                                 '录取概率': ['99.84%', '99.73%', '99.67%', '99.67%', '98.09%', '97.96%', '97.96%', '97.94%', '97.94%', '95.8%', '94.92%', '91.7%']} ,
#                     华南理工大学:{'批次': '本科第一批',
#                                 '专业列表': ['会计学', '材料类', '过程装备与控制工程', '计算机科学与技术', '建筑学', '食品科学与工程', '软件工程', '车辆工程', '工商管理类'],
#                                 '录取概率': ['99.84%', '98.44%', '98.09%', '95.8%', '95.8%', '91.7%', '91.7%', '91.7%', '91.7%']},
#                     四川大学:{'批次': '本科第一批',
#                              '专业列表': ['电气工程及其自动化', '高分子材料与工程', '临床药学', '核工程与核技术', '物理学类', '金融学类', '生物医学工程', '经济学类', '工商管理类', '口腔医学技术', '药学'],
#                              '录取概率': ['99.84%', '99.84%', '99.73%', '97.74%', '94.66%', '97.16%', '98.09%', '97.96%', '97.94%', '94.92%', '91.7%']} }