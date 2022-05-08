import random
import re
import time
import requests
from bs4 import  BeautifulSoup
import os
import  json
import pymysql

evpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/"
conn = pymysql.connect(
    host='sh-cynosdbmysql-grp-r7x6jnui.sql.tencentcdb.com',
    user='root',
    password='Hsx123456',
    database='qndxx',
    charset='utf8',
    port=29682
)
cursor = conn.cursor()
def spider(url,hed):
    respone=requests.get(url,headers=hed).text
    soup=BeautifulSoup(respone,'lxml')
    alllist=soup.findAll('div',attrs={"class":'card'})
    ahref=re.search(r'www.51daxuexi.com/detail/.+/',alllist[0].find('a')['href']).group()
    print(ahref)
    imgsrc=alllist[0].find('a').find('img')['src']
    atitle=alllist[0].find('a')['title']
    name=selectmysql()
    print(name)
    if name!=atitle:
        inmysql(atitle,ahref)
        photo=requests.get(imgsrc,headers=hed,verify=False).content
        with open(evpath+atitle+'.jpg','wb') as f:
            f.write(photo)
        upphoto(atitle+'.jpg',evpath+atitle+'.jpg')
    print("执行成功！")
    cursor.close()
    conn.close()

def selectmysql():

    sql='select qishuname from qdapp_num;'
    cursor.execute(sql)
    mysqlvalue =cursor.fetchall()
    return mysqlvalue[0][0]

def inmysql(title,href):
    sql="update  qdapp_num set qdlink='%s',qishuname='%s'  where id = 1;"%(href, title)
    cursor.execute(sql)
    conn.commit()
    print('插入成功！')
def upphoto(path,classstr):
    # 获取token

    data = {
        "env": "prod-7gs5ov3sf092d402",
        "path": "img/" + path
    }  # 需填入env和path
    # 转json
    data = json.dumps(data)
    response = requests.post("https://api.weixin.qq.com/tcb/uploadfile",data, verify=False)
    # 得到上传链接
    data2 = {
        "Content-Type": (None, ".zip"),  # 此处为上传文件类型
        "key": (None, "img/" + path),  # 需填入path
        "Signature": (None, response.json()['authorization']),
        'x-cos-security-token': (None, response.json()['token']),
        'x-cos-meta-fileid': (None, response.json()['cos_file_id']),
        'file': (path, open(classstr, "rb"))  # 需填入本地文件路径
    }
    response2 = requests.post(response.json()['url'], files=data2,verify=False)  # 此处files提交的为表单数据，不为json数据，json数据或其他数据会报错

if __name__=='__main__':
    url = 'https://www.51daxuexi.com/?page=1'
    hed = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"}
    while True:
        spider(url,hed)
        time.sleep(60*60*24)
