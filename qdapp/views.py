import os
import time
import zipfile
from datetime import datetime
import shutil
from django.http import HttpResponse
from django.shortcuts import render,redirect,reverse
from qdapp.models import Xinxi,Student,Fileid,Num
import json
import requests
# Create your views here.

qndxxlist=[i for i in range(1,16)]
evpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/static/img/'
#evpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'\\static\\img\\'
print(evpath)
def wy(request):
    student = Student.objects.filter(status=0)
    slist = [a.name for a in student]
    strlist = '、'.join(slist)
    number=Num.objects.filter(id=1)
    context={"qdlist": qndxxlist, 'student': strlist}
    for i in number:
        context['qdlink']=i.qdlink
        context['qishuname']=i.qishuname
        context['downfile']=downloadfile(i.file_id)
    return render(request, '1.html',context)

def do_wy(request):
    num=Num.objects.get(id=1)
    NUmber=num.num+1
    xinxidb=Xinxi()
    if num.num!=24:
        qishu=request.POST['qda']
            #wx_duixiangcunchu()
        name=request.POST['name']
        number=request.POST['number']
        #存入数据库
        xinxidb.name=name
        xinxidb.studentnum=number
        xinxidb.qishu=qishu
        xinxidb.create_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        xinxidb.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #存入session
        request.session['num']=1
        myfile=request.FILES.get("img")
        if not myfile:
            return HttpResponse("没有上传截图")
        cover_pic =number+ "." + myfile.name.split('.').pop()
        xinxidb.cover_pic=cover_pic
        destination = open(evpath+cover_pic, "wb+")
        for chunk in myfile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        xinxidb.save()
        try:
            db=Student.objects.get(name=name)
            db.status=1
            db.save()
        except:
            print('error')
        num.num=num.num+1
        num.save()
        classstr=evpath+cover_pic
        wx_duixiangcunchu(cover_pic, classstr)
    if NUmber==24:
        student=Student.objects.filter(status=1)
        student.update(status=0)
        num.num=0
        num.save()
    return redirect(reverse('app'))


def wx_duixiangcunchu(path,classstr):
      #获取token
    # response = requests.get(
    #       'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxc89ec0b61a9d8dae&secret=5c1e711a135a57233b60c4c27a22eda1')
    data ={
        "env": "prod-7gs5ov3sf092d402",
        "path": "image/"+path
      }#需填入env和path
    #转json
    data = json.dumps(data)
    # response = requests.post("https://api.weixin.qq.com/tcb/uploadfile?access_token="+response.json()['access_token'],data,verify = False)
    response = requests.post(
          "https://api.weixin.qq.com/tcb/uploadfile", data,
          verify=False)
      #得到上传链接
    data2={
        "Content-Type":(None,".zip"), #此处为上传文件类型
        "key": (None,"image/"+path), #需填入path
        "Signature": (None,response.json()['authorization']),
        'x-cos-security-token': (None,response.json()['token']),
        'x-cos-meta-fileid': (None,response.json()['cos_file_id']),
        'file': (path,open(classstr, "rb")) #需填入本地文件路径
        }
    response2 = requests.post(response.json()['url'], files=data2,verify = False) #此处files提交的为表单数据，不为json数据，json数据或其他数据会报错
    db=Fileid()
    db.name=path
    db.fileid=response.json()["file_id"]
    db.save()

def downloadfile(file_id):
    # response = requests.get(
    #     'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxc89ec0b61a9d8dae&secret=5c1e711a135a57233b60c4c27a22eda1', )

    data = {
        "env": "prod-7gs5ov3sf092d402",
        'file_list': [
            {'fileid': file_id
                , 'max_age': 60 * 60 * 24 * 8}]}
    # 转json
    data = json.dumps(data)
    response = requests.post(
        "https://api.weixin.qq.com/tcb/batchdownloadfile", data,verify=False)
    return response.json()["file_list"][0]['download_url']



