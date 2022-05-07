import os
import time
import zipfile
import datetime
import shutil
from django.http import HttpResponse
from django.shortcuts import render,redirect,reverse
from qdapp.models import Xinxi,Student,Fileid,Num
import json
import requests
# Create your views here.

qndxxlist=[i for i in range(1,16)]
evpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/static/img/'
print(evpath)
def wy(request):
    student = Student.objects.filter(status=0)
    slist = [a.name for a in student]
    strlist = '、'.join(slist)
    return render(request, '1.html', {"qdlist": qndxxlist, 'student': strlist})
def do_wy(request):
    num=Num.objects.get(id=1)
    NUmber=num.num+1
    print(NUmber)
    if num.num!=24:
        qishu=request.POST['qda']
        classstr="D20C050"+qishu+'青年大学习截图/'
        if os.path.exists(evpath+classstr)==False:
            os.makedirs(evpath+classstr)
            #wx_duixiangcunchu()
        name=request.POST['name']
        number=request.POST['number']
        myfile=request.FILES.get("img")
        if not myfile:
            return HttpResponse("没有上传截图")
        cover_pic = str(time.time()) + "." + myfile.name.split('.').pop()
        destination = open(evpath+classstr+cover_pic, "wb+")
        for chunk in myfile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        try:
            db=Student.objects.get(name=name)
            db.status=1
            db.save()
        except:
            print('error')
        num.num=num.num+1
        num.save()
    if NUmber==24:
        qishu=request.POST['qda']
        path="D20C050"+qishu+'青年大学习截图'
        classstr=evpath+path
        zipFile(classstr)
        print(path+'.zip',classstr+'.zip')
        a=wx_duixiangcunchu(path+'.zip',classstr+'.zip')
        os.remove(classstr+'.zip')
        shutil.rmtree(classstr)
        student=Student.objects.filter(status=1)
        student.update(status=0)
        num.num=0
        num.save()
    # return redirect(reverse('app'))
    return HttpResponse(a)

def wx_duixiangcunchu(path,classstr):
      #获取token
    response = requests.get('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxc89ec0b61a9d8dae&secret=5c1e711a135a57233b60c4c27a22eda1',verify = False) #需填入appid和AppSecret
    data ={
        "env": "prod-7gs5ov3sf092d402",
        "path": "image/"+path
      }#需填入env和path
    #转json
    data = json.dumps(data)
    return response.json()
    # response = requests.post("https://api.weixin.qq.com/tcb/uploadfile?access_token="+response.json()['access_token'],data,verify = False)
    #   #得到上传链接
    # data2={
    #     "Content-Type":(None,".zip"), #此处为上传文件类型
    #     "key": (None,"image/"+path), #需填入path
    #     "Signature": (None,response.json()['authorization']),
    #     'x-cos-security-token': (None,response.json()['token']),
    #     'x-cos-meta-fileid': (None,response.json()['cos_file_id']),
    #     'file': (path,open(classstr, "rb")) #需填入本地文件路径
    #     }
    # response2 = requests.post(response.json()['url'], files=data2,verify = False) #此处files提交的为表单数据，不为json数据，json数据或其他数据会报错
    # db=Fileid()
    # db.name=path
    # db.fileid=response.json()["file_id"]
    # db.save()

def zipFile(src_dir):
    zip_name = src_dir + '.zip'
    z = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(src_dir):
        fpath = dirpath.replace(src_dir, '')
        fpath = fpath and fpath + os.sep or ''
        for filename in filenames:
            z.write(os.path.join(dirpath, filename), fpath + filename)
        print('==压缩成功==')
    z.close()

