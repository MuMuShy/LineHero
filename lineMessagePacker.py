#打包資料格式

#打包info格式
import json


def getInfoFlexJson(user_name,user_img_link,user_money,locked_money,user_id):
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
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                            {
                                "type": "text",
                                "text": "ID:",
                                "color": "#aaaaaa",
                                "size": "sm",
                                "flex": 1
                            },
                            {
                                "type": "text",
                                "text": str(user_id),
                                "color": "#944dff",
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


def getHelpFlex():
    json = {
    "type": "bubble",
    "hero": {
        "type": "image",
        "url": "https://bukku.com.tw/wp-content/uploads/sites/6/2021/04/%E6%88%AA%E5%9C%96-2021-04-02-%E4%B8%8A%E5%8D%8812.56.22-300x298.png",
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
            "text": "通殺骰手",
            "weight": "bold",
            "size": "xl",
            "color": "#ff0000",
            "align": "center"
        },
        {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "spacing": "sm",
            "contents": [
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "房間列表",
                "text": "!gamelist"
                }
            },
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "創建房間",
                "text": "!create"
                }
            },
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "確認資料",
                "text": "!info"
                }
            },
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "排行榜",
                "text": "!ranking"
                }
            }
            ]
        }
        ]
    },
    "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
        {
            "type": "text",
            "text": "請勿沉迷賭博",
            "style": "italic",
            "weight": "bold",
            "decoration": "line-through",
            "align": "center"
        }
        ],
        "flex": 0
    }
    }
    return json


def getRanking(rank1,rank2,rank3,rank4,rank5):
    json = {
    "type": "bubble",
    "hero": {
        "type": "image",
        "url": "https://mumu.tw/images/ranking.jpg",
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
            "text": "通殺王",
            "weight": "bold",
            "size": "xl",
            "align": "center"
        },
        {
            "type": "text",
            "text": "1."+ rank1,
            "align": "center",
            "style": "normal",
            "weight": "bold",
            "color": "#e60000"
        },
        {
            "type": "text",
            "text": "2."+rank2,
            "style": "normal",
            "weight": "bold",
            "align": "center"
        },
        {
            "type": "text",
            "text": "3."+rank3,
            "style": "normal",
            "weight": "bold",
            "align": "center"
        },
        {
            "type": "text",
            "text": "4."+rank4,
            "style": "normal",
            "weight": "bold",
            "align": "center"
            
        },
        {
            "type": "text",
            "text": "5."+rank5,
            "style": "normal",
            "weight": "bold",
            "align": "center"
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
            "label": "來一把",
            "text": "!c"
            }
        }
        ],
        "flex": 0
    }
    }
    return json