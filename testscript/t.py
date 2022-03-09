from ftplib import FTP         #引入ftp模組
import os
import requests
from dotenv import load_dotenv
load_dotenv()

def uploadNewWeapon(url,id):
    ftp = FTP(os.getenv("FTPSERVER"))           #設定ftp伺服器地址
    ftp.login(os.getenv("FTPACCOUNT"),os.getenv("FTPPASSWORD"))      #設定登入賬戶和密碼
    ftp.cwd("./weapons")
    ftp.retrlines('LIST')          #列出檔案目錄       #選擇操作目錄
    ftp.retrlines('LIST')          #列出目錄檔案
    # localfile = '/mnt/NasFile/ftp測試/新功能.doc'    #設定檔案位置
    # f = open(localfile, 'rb')        #開啟檔案
    # ftp.storbinary('STOR %s' % os.path.basename(localfile), f) #上傳檔案

    with open(str(id)+".png", 'wb') as handle:
        response = requests.get(url, stream=True)
        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)

if __name__ == "__main__":
    uploadNewWeapon('https://www.ge-oku.com/3dstore/wp-content/uploads/2020/05/RunningSword3-300x300.png',12)