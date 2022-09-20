from django.db import models

# Create your models here.
class trainingSet(models.Model):
    place = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    year = models.IntegerField()
    school = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    major = models.CharField(max_length=255)
    line = models.IntegerField()
    score = models.IntegerField()
    rank = models.IntegerField()
    gap1 = models.IntegerField()
    gap2 = models.IntegerField()
    gap3 = models.IntegerField()

class yiFenYiDang(models.Model):
    place = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    score = models.IntegerField()
    rank = models.IntegerField()

class line(models.Model):
    place = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    line1 = models.IntegerField()
    line2 = models.IntegerField()
    line3 = models.IntegerField()

class school(models.Model):
    name = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    eryiyi = models.IntegerField()
    jiubawu = models.IntegerField()
    yuanxiaojuban = models.CharField(max_length=255)
    yuanxiaoleixing = models.CharField(max_length=255)
    yuanxiaolishu = models.CharField(max_length=255)
    banxueleixing = models.CharField(max_length=255)
    scorexyh = models.DecimalField(max_digits=11, decimal_places=2)
    scorewsl1 = models.DecimalField(max_digits=11, decimal_places=2)
    scorewsl2 = models.DecimalField(max_digits=11, decimal_places=2)
    scorewd1 = models.DecimalField(max_digits=11, decimal_places=2)
    scorewd2 = models.DecimalField(max_digits=11, decimal_places=2)
    esisubject = models.DecimalField(max_digits=11, decimal_places=2)
    esipaper = models.DecimalField(max_digits=11, decimal_places=2)
    employment = models.DecimalField(max_digits=11, decimal_places=2)

class places(models.Model):
    name=models.CharField(max_length=255)
    rank=models.DecimalField(max_digits=11, decimal_places=2)

class yuanxiaojuban(models.Model):
    name = models.CharField(max_length=255)
    rank = models.DecimalField(max_digits=11, decimal_places=2)

class yuanxiaoleixing(models.Model):
    name = models.CharField(max_length=255)
    rank = models.DecimalField(max_digits=11, decimal_places=2)

class yuanxiaolishu(models.Model):
    name = models.CharField(max_length=255)
    rank = models.DecimalField(max_digits=11, decimal_places=2)

class banxueleixing(models.Model):
    name = models.CharField(max_length=255)
    rank = models.DecimalField(max_digits=11, decimal_places=2)

class testXieTongGuoLv(models.Model):
    place = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    school = models.CharField(max_length=255)
    score = models.IntegerField()


PLACE_CHOICES = ( ('重庆', '重庆'),  ('河北', '河北'),('湖北', '湖北'),('贵州', '贵州') )
SUBJECT_CHOICES = ( ('理科', '理科'), ('文科', '文科'))
LINE_CHOICES = ((0, '不限批次'), (1, '本科第一批'), (2, '本科第二批'), (3, '专科'))
CITY_CHOICES = ((0,'不限省份'),('上海市','上海市'),('云南省','云南省'),('内蒙古自治区','内蒙古自治区'),
('北京市','北京市'),('吉林省','吉林省'),('四川省','四川省'),('天津市','天津市'),
('宁夏回族自治区','宁夏回族自治区'),('安徽省','安徽省'),('山东省','山东省'),('山西省','山西省'),
('广东省','广东省'),('广西壮族自治区','广西壮族自治区'),('新疆维吾尔自治区','新疆维吾尔自治区'),('江苏省','江苏省'),
('江西省','江西省'),('河北省','河北省'),('河南省','河南省'),('浙江省','浙江省'),
('海南省','海南省'),('湖北省','湖北省'),('湖南省','湖南省'),('澳门特别行政区','澳门特别行政区'),
('甘肃省','甘肃省'),('福建省','福建省'),('西藏自治区','西藏自治区'),('贵州省','贵州省'),
('辽宁省','辽宁省'),('重庆市','重庆市'),('陕西省','陕西省'),('青海省','青海省'),
('香港特别行政区','香港特别行政区'),('黑龙江省','黑龙江省'))
PAIXU_CHOICES = ((0,'匹配率'),(1,'综合排名'),('scorexyh','校友会排名'),('scorewsl','武书连排名'),
                            ('scorewd','网大排名'),('esi','ESI全球学科排名'),('emp','就业排名'))
