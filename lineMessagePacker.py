#打包資料格式

#打包info格式
import json


def getInfoFlexJson(user_name,user_type,user_img_link,user_money,locked_money,user_id,ranking):
    if str(user_img_link).startswith('http') is False:
        user_img_link = 'https://mumu.tw/images/game_ui/job_bkg.jpg'
    color = "#ff0000"
    if user_type != "GM":
        color = "#6666ff"
    json = {
    "type": "carousel",
    "contents": [
        {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "image",
                "url": user_img_link,
                "size": "full",
                "aspectMode": "cover",
                "aspectRatio": "2:3",
                "gravity": "top"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": user_name,
                        "size": "xl",
                        "color": "#ffffff",
                        "weight": "bold"
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                    {
                        "type": "text",
                        "text": "可用 $"+str("{:,}".format(user_money)),
                        "color": "#00b33c",
                        "size": "sm",
                        "flex": 0
                    }
                    ],
                    "spacing": "lg"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                    {
                        "type": "text",
                        "text": "鎖定 $"+str("{:,}".format(locked_money)),
                        "color": "#ff1a1a",
                        "flex": 0,
                        "size": "sm"
                    }
                    ],
                    "spacing": "lg"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "ID : "+str(user_id),
                        "color": "#ffffff"
                    }
                    ]
                },
                {
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "玩一把",
                    "text": "!create"
                    },
                    "style": "primary",
                    "margin": "none"
                },
                {
                    "type": "separator",
                    "margin": "sm",
                    "color": "#ffffff00"
                },{
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "冒險者之旅",
                    "text": "@jobinfo"
                    },
                    "style": "primary",
                    "margin": "none"
                }
                ],
                "position": "absolute",
                "offsetBottom": "0px",
                "offsetStart": "0px",
                "offsetEnd": "0px",
                "backgroundColor": "#00000090",
                "paddingAll": "20px",
                "paddingTop": "18px"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "color": "#ffffff",
                    "align": "center",
                    "size": "xs",
                    "offsetTop": "4.5px",
                    "text": user_type
                }
                ],
                "position": "absolute",
                "cornerRadius": "20px",
                "offsetTop": "18px",
                "backgroundColor": color,
                "offsetStart": "18px",
                "height": "25px",
                "width": "53px"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "color": "#ffffff",
                    "align": "center",
                    "size": "xxs",
                    "text": "排名: "+str(ranking),
                    "style": "normal",
                    "offsetTop": "5px",
                    "weight": "bold"
                }
                ],
                "position": "absolute",
                "cornerRadius": "20px",
                "offsetTop": "18px",
                "backgroundColor": "#3366cc",
                "offsetStart": "200px",
                "height": "25px",
                "width": "90px"
            }
            ],
            "paddingAll": "0px"
        }
        }
    ]
    }
    return json


def getDiceResult(num):
    _diceurl = str(num)
    if int(num) == 6:
        _diceurl = "60"
    json = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": "https://mumu.tw/images/dice/dice"+_diceurl+".jpg",
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
    "type": "carousel",
    "contents": [
        {
        "type": "bubble",
        "size": "micro",
        "hero": {
            "type": "image",
            "url": "https://mumu.tw/images/dice/daily.jpg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "320:213"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "每日獎賞",
                "weight": "bold",
                "size": "sm",
                "wrap": True
            },
            {
                "type": "box",
                "layout": "baseline",
                "contents": [
                {
                    "type": "text",
                    "text": "每天都先點我一下吧!",
                    "size": "xs",
                    "color": "#8c8c8c",
                    "margin": "md",
                    "flex": 0,
                    "align": "start"
                }
                ]
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "contents": []
                },
                {
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "點我",
                    "text": "!dailyrequest"
                    }
                }
                ]
            }
            ],
            "spacing": "sm",
            "paddingAll": "13px"
        }
        },
        {
        "type": "bubble",
        "size": "micro",
        "hero": {
            "type": "image",
            "url": "https://mumu.tw/images/dice/startroll.jpg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "320:213"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "開始遊戲",
                "weight": "bold",
                "size": "sm",
                "wrap": True
            },
            {
                "type": "box",
                "layout": "baseline",
                "contents": [
                {
                    "type": "text",
                    "text": "開始一場擲骰遊戲",
                    "size": "xs",
                    "color": "#8c8c8c",
                    "margin": "md",
                    "flex": 0
                }
                ]
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "創建房間",
                    "text": "!create"
                    }
                }
                ]
            }
            ],
            "spacing": "sm",
            "paddingAll": "13px"
        }
        },
        {
        "type": "bubble",
        "size": "micro",
        "hero": {
            "type": "image",
            "url": "https://mumu.tw/images/dice/jpselect.jpg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "320:213"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "幸運抽獎",
                "weight": "bold",
                "size": "sm"
            },
            {
                "type": "box",
                "layout": "baseline",
                "contents": [
                {
                    "type": "text",
                    "text": "一次$100拼大獎!",
                    "size": "xs",
                    "color": "#8c8c8c",
                    "margin": "md",
                    "flex": 0
                }
                ]
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "查看獎池",
                    "text": "!watherprice"
                    }
                }
                ]
            }
            ],
            "spacing": "sm",
            "paddingAll": "13px"
        }
        },
        {
        "type": "bubble",
        "size": "micro",
        "hero": {
            "type": "image",
            "url": "https://mumu.tw/images/dice/person.png",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "320:213"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "個人資訊",
                "weight": "bold",
                "size": "sm"
            },
            {
                "type": "box",
                "layout": "baseline",
                "contents": [
                {
                    "type": "text",
                    "text": "查看使用者資料",
                    "size": "xs",
                    "color": "#8c8c8c",
                    "margin": "md",
                    "flex": 0
                }
                ]
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "查看個人資料",
                    "text": "!info"
                    }
                }
                ]
            }
            ],
            "spacing": "sm",
            "paddingAll": "13px"
        }
        },
        {
        "type": "bubble",
        "size": "micro",
        "hero": {
            "type": "image",
            "url": "https://mumu.tw/images/dice/ranking.jpg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "320:213"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "排行榜",
                "weight": "bold",
                "size": "sm"
            },
            {
                "type": "box",
                "layout": "baseline",
                "contents": [
                {
                    "type": "text",
                    "text": "分數排行榜",
                    "size": "xxs",
                    "color": "#8c8c8c",
                    "margin": "md",
                    "flex": 0
                }
                ]
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "查看排行榜",
                    "text": "!ranking"
                    }
                }
                ]
            }
            ],
            "spacing": "sm",
            "paddingAll": "13px"
        }
        },
        {
        "type": "bubble",
        "size": "micro",
        "hero": {
            "type": "image",
            "url": "https://mumu.tw/images/dice/roomlist.png",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "320:213"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "房間列表",
                "weight": "bold",
                "size": "sm"
            },
            {
                "type": "box",
                "layout": "baseline",
                "contents": [
                {
                    "type": "text",
                    "text": "列出所有房間",
                    "size": "xxs",
                    "color": "#8c8c8c",
                    "margin": "md",
                    "flex": 0
                }
                ]
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "查看",
                    "text": "!gamelist"
                    }
                }
                ]
            }
            ],
            "spacing": "sm",
            "paddingAll": "13px"
        }
        },
        {
        "type": "bubble",
        "size": "micro",
        "hero": {
            "type": "image",
            "url": "https://mumu.tw/images/dice/history.png",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "320:213"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "歷史擲骰",
                "weight": "bold",
                "size": "sm"
            },
            {
                "type": "box",
                "layout": "baseline",
                "contents": [
                {
                    "type": "text",
                    "text": "所有擲骰結果",
                    "size": "xxs",
                    "color": "#8c8c8c",
                    "margin": "md",
                    "flex": 0
                }
                ]
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "查看",
                    "text": "!rollhistory"
                    }
                }
                ]
            }
            ],
            "spacing": "sm",
            "paddingAll": "13px"
        }
        }
    ]
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


def getDiceBetChoose():
    json = {
        "type": "carousel",
        "contents": [
            {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "純數字 倍率:*5",
                    "color": "#ffffff",
                    "align": "start",
                    "size": "md",
                    "gravity": "center"
                },
                {
                    "type": "text",
                    "text": "16%",
                    "color": "#ffffff",
                    "align": "start",
                    "size": "xs",
                    "gravity": "center",
                    "margin": "lg"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "filler"
                        }
                        ],
                        "width": "16%",
                        "backgroundColor": "#0D8186",
                        "height": "6px"
                    }
                    ],
                    "backgroundColor": "#9FD8E36E",
                    "height": "6px",
                    "margin": "sm"
                }
                ],
                "backgroundColor": "#27ACB2",
                "paddingTop": "19px",
                "paddingAll": "12px",
                "paddingBottom": "16px"
            },
            "body": {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "1",
                    "text": "!j 1:1000"
                    }
                },
                {
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "2",
                    "text": "!j 2:1000"
                    }
                },
                {
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "3",
                    "text": "!j 3:1000"
                    }
                },
                {
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "4",
                    "text": "!j 4:1000"
                    }
                },
                {
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "5",
                    "text": "!j 5:1000"
                    }
                },
                {
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "6",
                    "text": "!j 6:1000"
                    }
                }
                ]
            },
            "styles": {
                "footer": {
                "separator": False
                }
            }
            },
            {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "大中小 倍率:*2.6",
                    "color": "#ffffff",
                    "align": "start",
                    "size": "md",
                    "gravity": "center"
                },
                {
                    "type": "text",
                    "text": "33%",
                    "color": "#ffffff",
                    "align": "start",
                    "size": "xs",
                    "gravity": "center",
                    "margin": "lg"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "filler"
                        }
                        ],
                        "width": "33%",
                        "backgroundColor": "#DE5658",
                        "height": "6px"
                    }
                    ],
                    "backgroundColor": "#FAD2A76E",
                    "height": "6px",
                    "margin": "sm"
                }
                ],
                "backgroundColor": "#FF6B6E",
                "paddingTop": "19px",
                "paddingAll": "12px",
                "paddingBottom": "16px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "button",
                        "action": {
                        "type": "message",
                        "label": "大",
                        "text": "!j 大:1000"
                        }
                    },
                    {
                        "type": "button",
                        "action": {
                        "type": "message",
                        "label": "中",
                        "text": "!j 中:1000"
                        }
                    },
                    {
                        "type": "button",
                        "action": {
                        "type": "message",
                        "label": "小",
                        "text": "!j 小:1000"
                        }
                    }
                    ],
                    "flex": 1
                }
                ],
                "spacing": "md",
                "paddingAll": "12px"
            },
            "styles": {
                "footer": {
                "separator": False
                }
            }
            },
            {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "單雙 倍率:*1.9",
                    "color": "#ffffff",
                    "align": "start",
                    "size": "md",
                    "gravity": "center"
                },
                {
                    "type": "text",
                    "text": "50%",
                    "color": "#ffffff",
                    "align": "start",
                    "size": "xs",
                    "gravity": "center",
                    "margin": "lg"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "filler"
                        }
                        ],
                        "width": "50%",
                        "backgroundColor": "#7D51E4",
                        "height": "6px"
                    }
                    ],
                    "backgroundColor": "#9FD8E36E",
                    "height": "6px",
                    "margin": "sm"
                }
                ],
                "backgroundColor": "#A17DF5",
                "paddingTop": "19px",
                "paddingAll": "12px",
                "paddingBottom": "16px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "button",
                        "action": {
                        "type": "message",
                        "label": "單",
                        "text": "!j 單:1000"
                        }
                    },
                    {
                        "type": "button",
                        "action": {
                        "type": "message",
                        "label": "雙",
                        "text": "!j 雙:1000"
                        }
                    }
                    ],
                    "flex": 1
                }
                ],
                "spacing": "md",
                "paddingAll": "12px"
            },
            "styles": {
                "footer": {
                "separator": False
                }
            }
            }
        ]
        }
    return json


def getRollDiceFlex():
    json = {
    "type": "bubble",
    "size": "nano",
    "hero": {
        "type": "image",
        "url": "https://mumu.tw/images/dice/roll.jpg",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "action": {
        "type": "uri",
        "uri": "http://linecorp.com/"
        }
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
            "label": "開骰!",
            "text": "!d"
            }
        }
        ],
        "flex": 0
    }
    }
    return json


def getDiceHistoryFlex(history):
    json = {
    "type": "carousel",
    "contents": [
        {
        "type": "bubble",
        "size": "kilo",
        "direction": "ltr",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "歷史擲骰結果",
                "color": "#ffffff",
                "align": "center",
                "size": "md",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": history,
                "weight": "bold",
                "color": "#ffffff",
                "align": "center"
            }
            ],
            "backgroundColor": "#27ACB2",
            "paddingTop": "19px",
            "paddingAll": "12px",
            "paddingBottom": "16px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "text",
                    "text": "此紀錄為所有與此機器人進行遊戲的結果.",
                    "color": "#8C8C8C",
                    "size": "sm",
                    "wrap": True
                }
                ],
                "flex": 1
            }
            ],
            "spacing": "md",
            "paddingAll": "12px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "來一把!",
                "text": "!c"
                }
            }
            ]
        },
        "styles": {
            "footer": {
            "separator": False
            }
        }
        }
    ]
    }
    return json


def getJackPotFlex(_jpjson):
    _total = _jpjson['grand']+_jpjson['major']+_jpjson['minor']+_jpjson['mini']
    json = {
    "type": "bubble",
    "hero": {
        "type": "image",
        "url": "https://img.freepik.com/free-vector/jackpot-background-with-flying-golden-coins_1017-23144.jpg?size=626&ext=jpg",
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
            "text": "- JACKPOT -",
            "weight": "bold",
            "size": "xl",
            "align": "center",
            "style": "normal",
            "decoration": "none",
            "color": "#ffffff"
        },
        {
            "type": "box",
            "layout": "vertical",
            "margin": "md",
            "contents": [
            {
                "type": "text",
                "text": "Grand: $"+str("{:,.2f}".format(_jpjson['grand'])),
                "size": "sm",
                "color": "#ff0000",
                "align": "center",
                "margin": "md",
                "flex": 0
            },
            {
                "type": "text",
                "text": "Major: $"+str("{:,.2f}".format(_jpjson['major'])),
                "size": "sm",
                "color": "#ff99cc",
                "align": "center",
                "margin": "md",
                "flex": 0
            },
            {
                "type": "text",
                "text": "Minor: $"+str("{:,.2f}".format(_jpjson['minor'])),
                "size": "sm",
                "color": "#6666ff",
                "align": "center",
                "margin": "md",
                "flex": 0
            },
            {
                "type": "text",
                "text": "Mini: $"+str("{:,.2f}".format(_jpjson['mini'])),
                "size": "sm",
                "color": "#ffff99",
                "align": "center",
                "margin": "md",
                "flex": 0
            },
            {
                "type": "separator"
            }
            ]
        },
        {
            "type": "box",
            "layout": "vertical",
            "margin": "md",
            "contents": [
            {
                "type": "text",
                "text": "Last Win:"+str(_jpjson['last_winner'])+" $ "+str("{:,.2f}".format(_jpjson['last_win']))+" !!!",
                "size": "xxs",
                "align": "center",
                "color": "#FFFFFF"
            },
            {
                "type": "separator"
            }
            ]
        },
        {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "spacing": "sm",
            "contents": [
            {
                "type": "text",
                "text": "累積金額:",
                "weight": "bold",
                "color": "#FFFFFF"
            },
            {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                {
                    "type": "text",
                    "text": "$: "+str("{:,.2f}".format(_total)),
                    "wrap": True,
                    "color": "#ff0000",
                    "size": "lg",
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
                    "text": "跟我玩拉霸機就有機會把獎金帶走!",
                    "wrap": True,
                    "color": "#FFFFFF",
                    "size": "xxs",
                    "flex": 5
                }
                ]
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
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
            "type": "message",
            "label": "$100 SPIN X1",
            "text": "!spin 1"
            }
        },
        {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
            "type": "message",
            "label": "$1000 SPINX10",
            "text": "!spin 10"
            }
        },
        {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
            "type": "message",
            "label": "$10000 SPINX100",
            "text": "!spin 100"
            }
        }
        ],
        "flex": 0
    },
    "styles": {
        "body": {
        "backgroundColor": "#660000"
        }
    }
    }
    return json

def getBugReport():
    json = {
    "type": "bubble",
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "text",
            "text": "BUG回報&建議",
            "weight": "bold",
            "color": "#1DB446",
            "size": "sm"
        },
        {
            "type": "text",
            "text": "感謝您的遊玩",
            "weight": "bold",
            "size": "xxl",
            "margin": "md"
        },
        {
            "type": "text",
            "text": "目前遊戲還只是開發階段,有一些有趣的小東西都在慢慢實現,怪物的圖片等等也會在未來進行外包的方式取得",
            "size": "xs",
            "color": "#aaaaaa",
            "wrap": True
        },
        {
            "type": "separator",
            "margin": "xxl"
        },
        {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "text",
                    "text": "LINE: @mumustudio",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                }
                ]
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "text",
                    "text": "E-MAIL:  mumushy850421@gmail.com",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                }
                ]
            },
            {
                "type": "separator",
                "margin": "xxl"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "margin": "xxl",
                "contents": [
                {
                    "type": "text",
                    "text": "python後端工程師",
                    "size": "sm",
                    "color": "#555555"
                }
                ]
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "text",
                    "text": "前端工程師",
                    "size": "sm",
                    "color": "#555555"
                }
                ]
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "text",
                    "text": "美術設計(2d)",
                    "size": "sm",
                    "color": "#555555"
                }
                ]
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "text",
                    "text": "遊戲企劃",
                    "size": "sm",
                    "color": "#555555"
                }
                ]
            }
            ]
        },
        {
            "type": "separator",
            "margin": "xxl"
        },
        {
            "type": "box",
            "layout": "vertical",
            "contents": []
        },
        {
            "type": "box",
            "layout": "vertical",
            "margin": "md",
            "contents": [
            {
                "type": "text",
                "text": "遊戲中如有任何素材疑慮請立即聯繫我們 ",
                "size": "xs",
                "color": "#aaaaaa",
                "flex": 0
            },
            {
                "type": "text",
                "text": "也歡迎有上述技能的小夥伴加入開發團隊",
                "size": "xs",
                "color": "#aaaaaa",
                "flex": 0
            }
            ]
        }
        ]
    },
    "styles": {
        "footer": {
        "separator": True
        }
    }
    }
    return json

def getPostButtonTest(user_line_id):
    json = {
    "type": "bubble",
    "hero": {
        "type": "image",
        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
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
            "text": "Brown Cafe",
            "weight": "bold",
            "size": "xl"
        },
        {
            "type": "box",
            "layout": "baseline",
            "margin": "md",
            "contents": [
            {
                "type": "icon",
                "size": "sm",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
            },
            {
                "type": "icon",
                "size": "sm",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
            },
            {
                "type": "icon",
                "size": "sm",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
            },
            {
                "type": "icon",
                "size": "sm",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
            },
            {
                "type": "icon",
                "size": "sm",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
            },
            {
                "type": "text",
                "text": "4.0",
                "size": "sm",
                "color": "#999999",
                "margin": "md",
                "flex": 0
            }
            ]
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
                    "text": "Place",
                    "color": "#aaaaaa",
                    "size": "sm",
                    "flex": 1
                },
                {
                    "type": "text",
                    "text": "Miraina Tower, 4-1-6 Shinjuku, Tokyo",
                    "wrap": True,
                    "color": "#666666",
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
                    "text": "Time",
                    "color": "#aaaaaa",
                    "size": "sm",
                    "flex": 1
                },
                {
                    "type": "text",
                    "text": "10:00 - 23:00",
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5
                }
                ]
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
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
            "type": "postback",
            "label": "action",
            "data": user_line_id
            }
        },
        {
            "type": "box",
            "layout": "vertical",
            "contents": [],
            "margin": "sm"
        }
        ],
        "flex": 0
    }
    }
    return json
