#打包資料格式

#打包info格式
import json


def getInfoFlexJson(user_name,user_img_link,user_money,locked_money):
    json = {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": user_img_link,
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover",
                    "action": {
                    "type": "uri",
                    "uri": "http://linecorp.com/"
                    }
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": user_name,
                        "weight": "bold",
                        "size": "xl"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                            {
                                "type": "text",
                                "text": "可用",
                                "color": "#aaaaaa",
                                "size": "sm",
                                "flex": 1
                            },
                            {
                                "type": "text",
                                "text": "$"+str(user_money),
                                "color": "#00e600",
                                "size": "sm",
                                "flex": 5
                            }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                            {
                                "type": "text",
                                "text": "鎖定",
                                "color": "#aaaaaa",
                                "size": "sm",
                                "flex": 1
                            },
                            {
                                "type": "text",
                                "text": "$"+str(locked_money),
                                "color": "#ff1a1a",
                                "size": "sm",
                                "flex": 5
                            }
                            ]
                        }

                        
                        ]
                    }
                    ]
                }
            }
    return json


def getDiceResult(num):
    json = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": "https://mumu.tw/images/dice/dice"+str(num)+".jpg",
            "size": "full",
            "aspectRatio": "5:4",
            "aspectMode": "cover",
            "action": {
            "type": "uri",
            "uri": "http://linecorp.com/"
            }
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "結果",
                "weight": "bold",
                "size": "xl"
            },
            {
                "type": "text",
                "text": str(num),
                "color": "#e60000",
                "align": "center",
                "style": "normal",
                "weight": "bold",
                "size": "lg"
            }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                "type": "message",
                "label": "點我再來一局",
                "text": "!create"
                }
            }
            ],
            "flex": 0
        }
        }
    return json
