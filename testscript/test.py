import os
import psycopg2
from dotenv import load_dotenv

from tDataBase import DataBase
database = DataBase()
load_dotenv()
DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
sql = "SELECT * from gameInfo"
cursor = conn.cursor()
cursor.execute(sql)
result = cursor.fetchall()
print(result)

# 事物提交
conn.commit()
# 關閉資料庫連線
conn.close()
