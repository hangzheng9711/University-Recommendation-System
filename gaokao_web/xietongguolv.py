'''
基于用户的协同过滤推荐算法
'''

from math import sqrt,pow
import operator

class UserCf():

    #获得初始化数据
    def __init__(self,data):
        self.data=data;

    #计算两个用户的欧式距离相似性
    def euclideanDistanceSim(self,user1,user2):
        x=sqrt(pow(user1['score']-user2['score'],2)+pow(user1['rank']-user2['rank'],2)+pow(user1['gap']-user2['gap'],2))
        max=sqrt(pow(650,2)+pow(120000,2)+pow(700,2))
        return ((max-x)/max)

    #计算与当前用户的相似度，获得最相似的N个用户
    def nearestUser(self,user,key,value):#key为0，表示使用阈值法；key为1，表示使用KNN最近邻算法；value为阈值或K值
        distances={}#最相似的N个用户，数据格式{1:0.92,4:0.97}，1,4表示self.data列表中的索引，小数表示相似率
        number=0;
        if key==0:
            for i in self.data:#遍历整个数据集
                distance=self.euclideanDistanceSim(i,user)#计算两个用户的相似度
                if distance>=value:
                   distances[number]=distance
                number=number+1
            sortedDistance=sorted(distances.items(),key=operator.itemgetter(1),reverse=True);#最相似的N个用户
            return sortedDistance
        else:
            for i in self.data:#遍历整个数据集
                distance=self.euclideanDistanceSim(i,user)#计算两个用户的相似度
                distances[number]=distance
                number=number+1
            sortedDistance=sorted(distances.items(),key=operator.itemgetter(1),reverse=True);#最相似的N个用户
            return sortedDistance[:value]

    #计算最相似的N个用户的学校对当前用户的录取概率，获得录取概率最高的学校
    def recommand(self,user,key,value):
        recommandList={}#录取概率最高的学校，数据格式{'四川大学':{'专业列表':[1,2],'录取概率':[0.92,0.93],'批次':1},......}
        distances=self.nearestUser(user,key,value)
        for otheruser,distance in dict(distances).items():#最相似的n个用户
                    if self.data[otheruser]['school'] not in recommandList.keys():#将学校、批次和专业、录取概率添加到推荐列表
                        recommandList[self.data[otheruser]['school']]={}
                        if self.data[otheruser]['line'] == 1:
                            recommandList[self.data[otheruser]['school']]['批次'] = '本科第一批'
                        elif self.data[otheruser]['line'] == 2:
                            recommandList[self.data[otheruser]['school']]['批次'] = '本科第二批'
                        else:
                            recommandList[self.data[otheruser]['school']]['批次'] = '专科'
                        recommandList[self.data[otheruser]['school']]['专业列表']=[]
                        recommandList[self.data[otheruser]['school']]['专业列表'].append(self.data[otheruser]['major'])
                        recommandList[self.data[otheruser]['school']]['录取概率']=[]
                        recommandList[self.data[otheruser]['school']]['录取概率'].append(distance)
                    elif self.data[otheruser]['major'] not in recommandList[self.data[otheruser]['school']]['专业列表']:
                        #学校和批次已经添加到推荐列表，将专业和录取概率添加到推荐列表
                        recommandList[self.data[otheruser]['school']]['专业列表'].append(self.data[otheruser]['major'])
                        recommandList[self.data[otheruser]['school']]['录取概率'].append(distance)
                    elif self.data[otheruser]['major'] in recommandList[self.data[otheruser]['school']]['专业列表']:
                        #学校和批次和专业已经添加到推荐列表，将推荐列表中的录取概率更新
                        position = recommandList[self.data[otheruser]['school']]['专业列表'].index(self.data[otheruser]['major'])
                        recommandList[self.data[otheruser]['school']]['录取概率'][position] = (recommandList[self.data[otheruser]['school']]['录取概率'][position]+distance)/2
        return recommandList

#if __name__=='__main__':
#    users = [{'school': '四川大学', 'major': '计算机科学与技术', 'line':1, 'score': 640, 'rank': 40000, 'gap': 70},
#             {'school': '北京大学', 'major': '化学', 'line':1, 'score': 700, 'rank': 3, 'gap': 140},
#             {'school': '北京理工大学', 'major': '物理', 'line':1, 'score': 650, 'rank': 30000, 'gap': 80},
#             {'school': '四川大学', 'major': '临床医学', 'line':1, 'score': 680, 'rank': 2000, 'gap': 110},
#             {'school': '南开大学', 'major': '电子信息', 'line':1, 'score': 670, 'rank': 1500, 'gap': 90},]

#    userCf=UserCf(data=users)
#    recommandList=userCf.recommand({'score': 643, 'rank': 40300, 'gap': 73})
#    print("推荐：%s" %recommandList)

#    推荐：
#    {'四川大学': {'批次': '本科第一批', '专业列表': ['计算机科学与技术', '临床医学'],
#    '录取概率': [0.999999995715267, 0.9593742892916977]},
#    '北京理工大学': {'批次': '本科第一批', '专业列表': ['物理'],
#    '录取概率': [0.9999907659707307]},
#    '南开大学': {'批次': '本科第一批', '专业列表': ['电子信息'], '录取概率': [0.9174279214505371]}}