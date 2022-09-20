from .models import school
from .models import places
from .models import yuanxiaojuban
from .models import yuanxiaoleixing
from .models import yuanxiaolishu
from .models import banxueleixing

from pylab import *
from numpy import *
import numpy as np
import operator
import math
import random

class FCM():

    #attribute_cal = ['place_rank', 'yxjb_rank', 'yxls_rank', 'bxlx_rank', '985', '211',
    #                 'employment', 'yxlx_rank', 'esisubject', 'esipaper', 'scorewsl2',
    #                 'scorewd2', 'scorewsl1', 'scorewd1', 'scorexyh']

    # 最大迭代数
    MAX_ITER = 100
    # 模糊参数
    m = 2.00

    #获得初始化数据
    def __init__(self, data):
        self.data=data;

    def getK(self,dangci,length):#分类数
        if dangci==4 and length>=7:
            k=6
        elif dangci==3 and length>=10:
            k=9
        elif dangci==2 and length>=13:
            k=12
        elif dangci==1 and length>=16:
            k=15
        else:
            k=3
        return k

    def getClassLabelandSampleList(self):
        sampleList=[]
        classLabel=[]
        for i in self.data:
            classLabel.append(i['学校'])
        length = len(classLabel)
        for i in range(0, length):
            everySchool = school.objects.get(name=classLabel[i])
            everySampleList=[]
            place_rank = places.objects.get(name=everySchool.place).rank
            everySampleList.append(float(place_rank))
            yxjb_rank = yuanxiaojuban.objects.get(name=everySchool.yuanxiaojuban).rank
            everySampleList.append(float(yxjb_rank))
            yxls_rank = yuanxiaolishu.objects.get(name=everySchool.yuanxiaolishu).rank
            everySampleList.append(float(yxls_rank))
            bxlx_rank = banxueleixing.objects.get(name=everySchool.banxueleixing).rank
            everySampleList.append(float(bxlx_rank))
            everySampleList.append(float(everySchool.jiubawu))
            everySampleList.append(float(everySchool.eryiyi))
            everySampleList.append(float(everySchool.employment))
            yxlx_rank = yuanxiaoleixing.objects.get(name=everySchool.yuanxiaoleixing).rank
            everySampleList.append(float(yxlx_rank))
            everySampleList.append(float(everySchool.esisubject))
            everySampleList.append(float(everySchool.esipaper))
            everySampleList.append(float(everySchool.scorewsl2))
            everySampleList.append(float(everySchool.scorewd2))
            everySampleList.append(float(everySchool.scorewsl1))
            everySampleList.append(float(everySchool.scorewd1))
            everySampleList.append(float(everySchool.scorexyh))
            sampleList.append(everySampleList)
        return classLabel,sampleList,length #length为样本数，classLabel为样本名['北京理工大学', '华南理工大学']

    # 初始化模糊矩阵U
    def initializeMembershipMatrix(self,length,k):#length为样本数为样本数
        membership_mat = list()
        for i in range(length):
            random_num_list = [random.random() for i in range(k)]
            summation = sum(random_num_list)
            temp_list = [x / summation for x in random_num_list]  # 首先归一化
            membership_mat.append(temp_list)
        return membership_mat

    # 计算类中心点
    def calculateClusterCenter(self,membership_mat,length,sampleList,k):#length为样本数
        cluster_mem_val = zip(*membership_mat)
        cluster_centers = list()
        cluster_mem_val_list = list(cluster_mem_val)
        for j in range(k):
            x = cluster_mem_val_list[j]
            xraised = [e ** self.m for e in x]
            denominator = sum(xraised)
            temp_num = list()
            for i in range(length):
                data_point = sampleList[i]
                prod = [xraised[i] * val for val in data_point]
                temp_num.append(prod)
            numerator = map(sum, zip(*temp_num))
            center = [z / denominator for z in numerator]  # 每一维都要计算。
            cluster_centers.append(center)
        return cluster_centers

    # 更新隶属度
    def updateMembershipValue(self,membership_mat, cluster_centers,length,sampleList,k):#length为样本数
        #    p = float(2/(m-1))
        data = []
        for i in range(length):
            x = sampleList[i]
            data.append(x)
            distances = [np.linalg.norm(list(map(operator.sub, x, cluster_centers[j]))) for j in range(k)]
            for j in range(k):
                den = sum([math.pow(float(distances[j] / distances[c]), 2) for c in range(k)])
                membership_mat[i][j] = float(1 / den)
        return membership_mat, data

    # 得到聚类结果
    def getClusters(self,membership_mat,length):#length为样本数
        cluster_labels = list()
        for i in range(length):
            max_val, idx = max((val, idx) for (idx, val) in enumerate(membership_mat[i]))
            cluster_labels.append(idx)
        return cluster_labels

    def fuzzyCMeansClustering(self,dangci):
        # 主程序
        class_labels,sampleList,length=self.getClassLabelandSampleList()
        k=self.getK(dangci,length)
        membership_mat = self.initializeMembershipMatrix(length,k)
        curr = 0
        while curr <= self.MAX_ITER:  # 最大迭代次数
            cluster_centers = self.calculateClusterCenter(membership_mat,length,sampleList,k)
            membership_mat, data = self.updateMembershipValue(membership_mat, cluster_centers,length,sampleList,k)
            cluster_labels = self.getClusters(membership_mat,length)
            curr += 1
        return class_labels,cluster_labels, cluster_centers,data,membership_mat

    def getFinalResultofCluster(self,dangci):
        class_labels,cluster_labels, cluster_centers,data,membership_mat=self.fuzzyCMeansClustering(dangci)
        cluster = []
         #遍历cluster_centers，获取dic(cluster1),dic(cluster2),dic(cluster3)......
        number1=0
        for i in cluster_centers:
                everyCluster={}
                everyCluster['高校位置']=int(i[0]*100)
                everyCluster['高校级别'] =int((i[1]+i[2]+i[3]+i[4]+i[5])/5*100)
                everyCluster['科学研究'] =int((i[8]+i[9]+i[10]+i[11])/4*100)
                everyCluster['人才培养'] =int((i[12]+i[13]+i[14])/3*100)
                everyCluster['就业'] =int((0.9*i[6]+0.1*i[7])*100)
                everyCluster['大学']=[]

                number2=0
                for j in cluster_labels:
                    if j==number1:
                        everyschool={}
                        everyschool['学校']=class_labels[number2]
                        everysingleschool=school.objects.get(name=everyschool['学校'])
                        everyschool['位置'] =everysingleschool.place
                        everyschool['院校举办']=everysingleschool.yuanxiaojuban
                        everyschool['院校隶属']=everysingleschool.yuanxiaolishu
                        everyschool['办学类型']=everysingleschool.banxueleixing
                        everyschool['院校类型']=everysingleschool.yuanxiaoleixing
                        if everysingleschool.jiubawu==1:
                            everyschool['985']="是"
                        else:
                            everyschool['985'] = "否"
                        if everysingleschool.eryiyi==1:
                            everyschool['211']="是"
                        else:
                            everyschool['211'] = "否"
                        everyschool['就业']=int(everysingleschool.employment*100)
                        everyschool['人才培养']=int((everysingleschool.scorewd1+everysingleschool.scorewsl1+everysingleschool.scorexyh)/3*100)
                        everyschool['科学研究']=int((everysingleschool.esisubject+everysingleschool.esipaper+everysingleschool.scorewd2+everysingleschool.scorewsl2)/4*100)
                        everyCluster['大学'].append(everyschool)
                    number2=number2+1

                cluster.append(everyCluster)
                number1=number1+1
        return cluster

    def xie_beni(self,dangci,length):
        class_labels, cluster_labels, cluster_centers, data, membership_mat = self.fuzzyCMeansClustering(dangci)
        center_array = array(cluster_centers)
        label = array(class_labels)
        datas = array(data)
        sum_cluster_distance = 0
        min_cluster_center_distance = inf
        k=self.getK(dangci,length)
        for i in range(k):
            for j in range(length):
                sum_cluster_distance = sum_cluster_distance + membership_mat[j][i] ** 2 * sum(
                    power(datas[j, :] - center_array[i, :], 2))  # 计算类一致性
        for i in range(k - 1):
            for j in range(i + 1, k):
                cluster_center_distance = sum(power(center_array[i, :] - center_array[j, :], 2))  # 计算类间距离
                if cluster_center_distance < min_cluster_center_distance:
                    min_cluster_center_distance = cluster_center_distance
        print(sum_cluster_distance / (length * min_cluster_center_distance))

