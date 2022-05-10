import json
import os
import zipfile
import pymysql
import requests


def selectmysql(qishu):
    sql = 'select cover_pic,name from qdapp_xinxi where qishu=qishu;'
    cursor.execute(sql)
    mysqlvalue = cursor.fetchall()
    return mysqlvalue

def fileid(mysqlvalue):
    fileid="cloud://prod-7gs5ov3sf092d402.7072-prod-7gs5ov3sf092d402-1306796063/image/"
    fileidlist=[]
    for i in mysqlvalue:
        fileiddict = {}
        fileiddict['fileid']=fileid+i[0]
        fileiddict['max_age']=60*60* 24*7
        fileidlist.append(fileiddict)
    return fileidlist

def getdownlink(fileidlist):
    response = requests.get(
        'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxc89ec0b61a9d8dae&secret=5c1e711a135a57233b60c4c27a22eda1',)
    data ={
        "env": "prod-7gs5ov3sf092d402",
        'file_list':fileidlist
    }#转json
    data = json.dumps(data)
    response = requests.post("https://api.weixin.qq.com/tcb/batchdownloadfile?access_token="+response.json()['access_token'],data)
    downlinklist=[b['download_url'] for b in response.json()["file_list"]]
    return downlinklist

def getphoto(list,mysqlvalue,qishu):
    filepath=r"C:\Users\hsx\Desktop\文件包\\"+"d20c050班青年大学习"+qishu+'截图'
    if  os.path.exists(filepath)==False:
        os.makedirs(filepath)
    hed = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"}
    for num in range(len(mysqlvalue)):
        cont=requests.get(list[num],headers=hed,verify=False).content
        with open(filepath+"\\"+mysqlvalue[num][1]+mysqlvalue[num][0],'wb+') as f:
            f.write(cont)
    zipFile(filepath)


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


if __name__=='__main__':
    qishu =input("请选期数：")
    conn = pymysql.connect(
        host='sh-cynosdbmysql-grp-r7x6jnui.sql.tencentcdb.com',
        user='root',
        password='Hsx123456',
        database='qndxx',
        charset='utf8',
        port=29682
    )
    cursor = conn.cursor()
    mysqlvalue=selectmysql(qishu)
    fileidlist=fileid(mysqlvalue)
    downlinklist=getdownlink(fileidlist)
    getphoto(downlinklist,mysqlvalue,qishu)
    delsql='delete from qdapp_xinxi where qishu=qishu;'
    cursor.execute(delsql)
    conn.commit()
    cursor.close()
    conn.close()