import pymysql
from settings import MYSQL_PORT,MYSQL_HOST,MYSQL_USER,MYSQL_PASSWD,MYSQL_DATABASE
from excel_ import get_data
from youdao import YOUDAO
import re
'''
整个程序流程
'''
class Demo:
    def __init__(self):
        self.db = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWD, database=MYSQL_DATABASE,
                             port=MYSQL_PORT, charset='utf8')  # 建立链接
        self.youdao=YOUDAO()#实例有道翻译模块
    def excel_data(self): #表格内容导入到数据库
        excle_generator=get_data('2-wp_posts.xlsx')#打开读取excel模块
        cursor=self.db.cursor()
        for valeu in excle_generator:
            conten = re.sub('<.*?>','',valeu[4])  # 第4个元素，文章内容#里面有html标签，剔除了，才能翻译
            title=valeu[5]
            sql = 'INSERT wp_posts(post_content,post_title)VALUES(%s,%s)'
            cursor.execute(sql, (conten, title))
            try:
                self.db.commit()
            except:
                db.rollback()
        cursor.close()
    def get_conten(self): #从数据库里面，把数据拿出来
        cursor=self.db.cursor()
        sql='SELECT ID,post_content,post_title FROM wp_posts'
        cursor.execute(sql)
        for i in cursor:
            yield i
        cursor.close()
    def updat_conten(self,id,conten,title):#更新数据库
        cursor = self.db.cursor()
        sql='UPDATE wp_posts SET post_content=%s,post_title=%s WHERE ID=%s'
        cursor.execute(sql,(conten,title,id))
        try:
            self.db.commit()
        except:
            self.db.rollback()
        cursor.close()  #游标要记得关闭
    def Chinese_to_English(self,i):#中文翻译成英文
        return self.youdao.translation(i,'zh-CHS','en')
    def English_to_Chinese(self,i):#因为翻译成中文
        return self.youdao.translation(i, 'en','zh-CHS')
    def run(self):
        get_conten=self.get_conten()
        for i in get_conten: #迭代这个迭代器，逐行获取数据
            title=self.Chinese_to_English(i[2])  #标题
            conten=self.Chinese_to_English((i[1]))#内容
            if conten and title:  #翻译以后，如果标题内容都不为空，说明都翻译成功了，更新数据库
                self.updat_conten(i[0],conten,title)
        for i in self.get_conten():#和上面步骤一样的，只不过把英文翻译中文
            title = self.English_to_Chinese(i[2])
            conten = self.English_to_Chinese((i[1]))
            if conten and title:
                self.updat_conten(i[0], conten, title)
        print('翻译完成')
if __name__ == '__main__':
    demo=Demo()
    # demo.excel_data()
    demo.run()


