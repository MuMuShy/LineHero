import random
from unittest.mock import patch
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
from ftplib import FTP
from dotenv import load_dotenv
load_dotenv()
FTPSERVER = os.environ['FTPSERVER']
FTPACCOUNT = os.environ['FTPACCOUNT']
FTPPASSWORD = os.environ['FTPPASSWORD']

def getRandomQuestionImage(user_line_id):
    import string
    import random
    number_of_strings = 1
    length_of_string = 4
    for x in range(number_of_strings):
        str = (''.join(random.choice(string.ascii_letters) for _ in range(length_of_string)))
        str = str.lower()
        print(str)
    createImg(str,user_line_id)
    return str


def getRandomColor():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)

def createImg(random_txt,user_line_id):

    bg_color = getRandomColor()
    # 創建一張隨機背景色的圖片
    img = Image.new(mode="RGB", size=(150, 70), color=bg_color)
    # 獲取圖片畫筆，用於描繪字
    draw = ImageDraw.Draw(img)
    # 修改字體
    font = ImageFont.truetype(font="arial.ttf", size=36)
    index = 0
    for char in random_txt:
        # 隨機生成5種字符+5種顏色
        random_txt = char
        txt_color = getRandomColor()
        # 避免文字顏色和背景色一致重合
        while txt_color == bg_color:
            txt_color = getRandomColor()
        # 根據坐標填充文字
        draw.text((10 + 30 * index, 3), text=random_txt, fill=txt_color, font=font)
        index+=1
    # 畫幹擾線點
    # draw.line(draw)
    # draw.point(draw)
    # 打開圖片操作，並保存在當前文件夾下
    path = os.getcwd()
    print(path)
    with open(path+"/"+user_line_id+".png", "wb") as f:
        img.save(f, format="png")
    
    uploadfile(path+"./"+user_line_id+".png")


def uploadfile(filename):
    ftp = FTP(FTPSERVER)           #設定ftp伺服器地址
    ftp.login(FTPACCOUNT, FTPPASSWORD)      #設定登入賬戶和密碼
    #ftp.retrlines('LIST')          #列出檔案目錄
    ftp.cwd('questions')            #選擇操作目錄
    #ftp.retrlines('LIST')          #列出目錄檔案
    localfile = filename    #設定檔案位置
    f = open(localfile, 'rb')        #開啟檔案
    #file_name=os.path.split(localfile)[-1]
    #ftp.storbinary('STOR %s'%file_name, f , 8192)
    ftp.storbinary('STOR %s' % os.path.basename(localfile), f) #上傳檔案

if __name__ == "__main__":
    answer = getRandomQuestionImage('123456')
