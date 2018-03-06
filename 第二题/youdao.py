import requests
from hashlib import md5
import time

'''
有道翻译模块
'''
class YOUDAO:
    def __init__(self):
        self.url='http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.headers={
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest',
            'Host':'fanyi.youdao.com',
            'Origin':'http://fanyi.youdao.com',
           'Referer':'http://fanyi.youdao.com/',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Connection':'keep-alive',

        }
        self.session=requests.session()
        self.get_inde()
    def get_inde(self):
        url='http://fanyi.youdao.com/'
        req=self.session.get(url)#先去首页获得一下cookie
    def translation(self,conten,forms,to):
        if len(conten)>5000:  #如果字数大于5000就不翻译了
            return None
        data={
            'i':conten,
            'from':forms,
            'to':to,
            'smartresult':'dict',
            'client':'fanyideskweb',
            'salt':int(time.time()*1000),
            'doctype':'json',
            'version':'2.1',
            'keyfrom':'fanyi.web',
            'action':'FY_BY_CLICKBUTTION',
            'typoResult':'false',
        }
        data['sign']=self.get_sign(data['salt'],conten)#加密获取sign，sign是md5加密
        req=self.session.post(self.url,data=data,headers=self.headers).json()
        conten=''
        for i in req['translateResult'][0]:
            conten+=i['tgt']
        if conten:
            return conten
    def get_sign(self,salt,conten):#sign的加密方法
        o="fanyideskweb" + conten+str(salt) + "ebSeFb%=XZ%T[KZ)c(sy!"
        md5_=md5()
        md5_.update(o.encode('utf-8'))
        return md5_ .hexdigest()


if __name__ == '__main__':
    youdao=YOUDAO()
    youdao.translation('你好')