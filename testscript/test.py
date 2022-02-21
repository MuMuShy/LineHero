import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

cursor = conn.cursor()
name ="test3"
id = "4123456789792138"
img ="http:123456"
sql ="SELECT user_line_id FROM users where user_line_name = '"+name+"'"

cursor.execute(sql)
print("successfully")
row = cursor.fetchone()
if row is not None:
    print(row)
else:
    sql ="""INSERT INTO users (user_line_name, user_line_id,user_img,user_money) VALUES (%(user_line_name)s, %(user_line_id)s, %(user_img)s, %(user_money)s)"""
    params = {'user_line_name':name, 'user_line_id':id,'user_img':img,'user_money':10000}
    cursor.execute(sql,params)
    print("successfully")

# 事物提交
conn.commit()
# 關閉資料庫連線
conn.close()