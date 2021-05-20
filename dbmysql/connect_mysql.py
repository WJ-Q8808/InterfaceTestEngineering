# -*- coding: utf-8 -*-# 
#-------------------------------------------------------------------------------
'''
豆瓣源
pip install Pyinstaller -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
（其中的Pyinstaller是你需要下载的库或包名，根据自己需求自行更改即可）
'''


import pymysql
from pprint import pprint
from config.loadconfig import ReadConfig

config_db = ReadConfig("config_db.json").read_file()

class DbConnect:
    def __init__(self,config_db,database=""):
        self.db_cfg = config_db
        self.db = pymysql.connect(database=database,
                                  #返回的数据改为"字典类型"（非必填）
                                  cursorclass=pymysql.cursors.DictCursor,
                                  **config_db)
        #获取db游标
        self.cursor = self.db.cursor()


    def select_sql(self,sql):
        """
        输入sql语句查下数据库
        sql = select * from phone_code where phone="+8617603033639" and create_time >"1594885094";
        :return: [{"uuid":"00pJDKYL"},{"email":"linzi477991@163.com"},{}.....]
        """
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def execute_sql(self,sql):
        """
        进行：增、删、改操作
        sql = inster into user (uuid,email) valuse ("udiajs1","email@ones.ai");
        sql = detele from phone_code where phone="+8617603033639" and create_time ="1594885094";
        sql = update user set email="email01@ones.ai" where uuid="udiajs1";
        :return:
        """
        try:
           self.cursor.execute(sql)
           self.db.commit()
        except:
            #如果执行失败就回滚
            self.db.rollback()

    def close(self):
        """
        关闭断开数据库操作
        """
        self.db.close()


# if __name__ == '__main__':
#     config_db = ReadConfig("config_db.json").read_file()
#     sql = '''select * from phone_code where phone = "+8617603033639" order by create_time desc limit 1;'''
#     database = "project_master"
#     DbConnect = DbConnect(config_db,database)
#     results = DbConnect.select_sql(sql)
#     if results:
#         print(results)
#     else:
#         print("This is null : {}".format(results))
#     DbConnect.close()



