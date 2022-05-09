from django.db import models
from datetime import datetime
# Create your models here.
class Xinxi(models.Model):
    name=models.CharField(max_length=250)
    studentnum=models.CharField(max_length=250)
    qishu=models.CharField(max_length=250)
    create_at = models.DateTimeField(default=datetime.now)  # 创建时间
    update_at = models.DateTimeField(default=datetime.now)
    cover_pic=models.CharField(max_length=250,default='')
class Fileid(models.Model):
    fileid=models.CharField(max_length=250)
    name=models.CharField(max_length=250)
class Student(models.Model):
    name=models.CharField(max_length=250)
    status=models.IntegerField(default=0) #0代表未交1代表已交
    def toDict(self):
        return {'name':self.name,'num':self.name}
class Num(models.Model):
    num=models.IntegerField()
    qishuname=models.CharField(max_length=250,null=True)
    qdlink=models.CharField(max_length=255,null=True)
    file_id=models.CharField(max_length=255,null=True)