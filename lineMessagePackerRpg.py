
import json


def getJobInfo(user_img_link,user_job_info,_rank):
    print(user_job_info)
    from Games import rpgGame 
    #userjobinfo = {"job","exp","hp","str","int","dex","level"}
    jobrul=""
    maxhp =0
    maxexp = rpgGame.getMaxExp(user_job_info["level"])
    
    if user_job_info['job'] == "warrior":
        maxhp = rpgGame.getMaxHp("warrior",user_job_info["level"])        
        jobrul = "https://mumu.tw/images/game_icons/icon_itemicon_sword.png"
    elif user_job_info['job'] == "majic":
        maxhp = rpgGame.getMaxHp("majic",user_job_info["level"])     
        jobrul = "https://mumu.tw/images/game_icons/icon_itemicon_book_magic.png"
    else:
        maxhp = rpgGame.getMaxHp("rog",user_job_info["level"])   
        jobrul = "https://mumu.tw/images/game_icons/icon_itemicon_arrow.png"
    if user_job_info["hp"] !=0:
        _hppersent = int((user_job_info["hp"]/maxhp)*100)
    else:
        _hppersent = 0
    if user_job_info["exp"] !=0:
        _exppersent = int((user_job_info["exp"]/maxexp)*100)
    else:
        _exppersent = 0
    _jobchinese = rpgGame.getjobChinese(user_job_info["job"])
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
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "image",
                            "url": jobrul,
                            "size": "xxs",
                            "align": "start",
                            "animated": True
                        }
                        ],
                        "width": "50px"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": _jobchinese+" LV:"+str(user_job_info["level"]),
                            "size": "xl",
                            "color": "#ffffff",
                            "align": "start",
                            "offsetTop": "xs"
                        }
                        ]
                    }
                    ]
                },
                {
                    "type": "text",
                    "text": "EXP",
                    "color": "#ffffff"
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
                        "width": str(_exppersent)+"%",
                        "backgroundColor": "#80ff80",
                        "height": "6px"
                    }
                    ],
                    "backgroundColor": "#FAD2A76E",
                    "margin": "sm",
                    "height": "6px"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                    {
                        "type": "text",
                        "text": str(user_job_info["exp"])+"/"+str(maxexp),
                        "color": "#00b33c",
                        "size": "sm",
                        "flex": 0
                    }
                    ],
                    "spacing": "lg"
                },
                {
                    "type": "text",
                    "text": "HP",
                    "color": "#ffffff"
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
                        "width": str(_hppersent)+"%",
                        "backgroundColor": "#ff1a1a",
                        "height": "6px"
                    }
                    ],
                    "backgroundColor": "#FAD2A76E",
                    "margin": "sm",
                    "height": "6px"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                    {
                        "type": "text",
                        "text": str(user_job_info["hp"])+"/"+str(maxhp),
                        "color": "#ff3333"
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                    {
                        "type": "text",
                        "text": "STR :"+str(user_job_info["str"])+"/ INT"+str(user_job_info["int"])+"/ DEX"+str(user_job_info["dex"]),
                        "color": "#ffffff",
                        "flex": 0,
                        "size": "sm"
                    }
                    ],
                    "spacing": "lg"
                },
                {
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "探索",
                    "text": "@exper"
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
                    "size": "xxs",
                    "text": "LV排名: "+str(_rank),
                    "style": "normal",
                    "offsetTop": "4.5px",
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
def getCheckJobButton():
    json={
    "type": "bubble",
    "size": "nano",
    "hero": {
        "type": "image",
        "url": "https://mumu.tw/images/game_icons/icon_itemicon_hero.png",
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
            "label": "查看",
            "text": "@jobinfo"
            }
        }
        ],
        "flex": 0
    }
    }
    return json
def getCreaterJobList():
    json = {
    "type": "carousel",
    "contents": [
        {
        "type": "bubble",
        "size": "nano",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "戰士",
                "color": "#ffffff",
                "align": "start",
                "size": "md",
                "gravity": "center"
            },
            {
                "type": "image",
                "url": "https://mumu.tw/images/game_icons/icon_itemicon_sword.png"
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
                    "text": "攻擊力一般,防禦優異,適合新手",
                    "color": "#8C8C8C",
                    "size": "sm",
                    "wrap": True
                }
                ],
                "flex": 1
            },
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "選擇",
                "text": "!initjob warrior"
                }
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
        "size": "nano",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "法師",
                "color": "#ffffff",
                "align": "start",
                "size": "md",
                "gravity": "center"
            },
            {
                "type": "image",
                "url": "https://mumu.tw/images/game_icons/icon_itemicon_book_magic.png"
            }
            ],
            "backgroundColor": "#ffcc00",
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
                    "text": "攻擊力中等,血量較低,適合技巧性玩家",
                    "color": "#8C8C8C",
                    "size": "sm",
                    "wrap": True
                }
                ],
                "flex": 1
            },
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "選擇",
                "text": "!initjob majic"
                }
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
        "size": "nano",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "盜賊",
                "color": "#ffffff",
                "align": "start",
                "size": "md",
                "gravity": "center"
            },
            {
                "type": "image",
                "url": "https://mumu.tw/images/game_icons/icon_itemicon_arrow.png"
            }
            ],
            "backgroundColor": "#ff1a1a",
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
                    "text": "攻擊力高爆擊率高,適合運氣高手",
                    "color": "#8C8C8C",
                    "size": "sm",
                    "wrap": True
                }
                ],
                "flex": 1
            },
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "選擇",
                "text": "!initjob rog"
                }
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


def getExperList():
    json = {
    "type": "carousel",
    "contents": [
        {
        "type": "bubble",
        "size": "nano",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "初始之森",
                "color": "#ffffff",
                "align": "start",
                "size": "md",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": "推薦LV: 1-10",
                "color": "#ffffff",
                "align": "start",
                "size": "xs",
                "gravity": "center",
                "margin": "lg"
            },
            {
                "type": "text",
                "text": "危險指數",
                "color": "#ffffff",
                "align": "start",
                "size": "xs",
                "gravity": "center",
                "margin": "xs"
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
                    "width": "10%",
                    "backgroundColor": "#ff0000",
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
            "layout": "vertical",
            "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "史萊姆",
                    "color": "#8C8C8C",
                    "size": "sm",
                    "wrap": True
                },
                {
                    "type": "text",
                    "text": "草原狼",
                    "color": "#8C8C8C",
                    "size": "sm",
                    "wrap": True
                },
                {
                    "type": "text",
                    "text": "野豬",
                    "color": "#8C8C8C",
                    "size": "sm",
                    "wrap": True
                },
                {
                    "type": "text",
                    "text": "隱藏腳色",
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
                "label": "出發",
                "text": "@goto forest"
                },
                "margin": "xs",
                "style": "primary",
                "offsetBottom": "10px",
                "height": "sm"
            }
            ],
            "spacing": "sm",
            "height": "50px"
        },
        "styles": {
            "footer": {
            "separator": False
            }
        }
        },
        {
        "type": "bubble",
        "size": "nano",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "墮落街口",
                "color": "#ffffff",
                "align": "start",
                "size": "md",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": "推薦LV: 8-20",
                "color": "#ffffff",
                "align": "start",
                "size": "xs",
                "gravity": "center",
                "margin": "lg"
            },
            {
                "type": "text",
                "text": "危險指數",
                "color": "#ffffff",
                "align": "start",
                "size": "xs",
                "gravity": "center",
                "margin": "xs"
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
                    "width": "30%",
                    "backgroundColor": "#ff0000",
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
            "layout": "vertical",
            "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "地鐵癡漢",
                    "color": "#8C8C8C",
                    "size": "sm",
                    "wrap": True
                },
                {
                    "type": "text",
                    "text": "扒手",
                    "color": "#8C8C8C",
                    "size": "sm",
                    "wrap": True
                },
                {
                    "type": "text",
                    "text": "小混混",
                    "color": "#8C8C8C",
                    "size": "sm",
                    "wrap": True
                },
                {
                    "type": "text",
                    "text": "隱藏腳色",
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
                "label": "封閉中..",
                "text": "@goto subway"
                },
                "margin": "xs",
                "style": "primary",
                "offsetBottom": "10px",
                "height": "sm"
            }
            ],
            "spacing": "sm",
            "height": "50px"
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


def getMonsterPacker(monster_json,now_hp):
    _url = "https://mumu.tw/images/monstersimg/"+str(monster_json["monster_id"])+".jpg"
    json = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": _url,
            "size": "full",
            "aspectRatio": "3:2",
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
                "text": monster_json["monster_name"],
                "weight": "bold",
                "size": "xl",
                "align": "center",
                "decoration": "underline"
            },
            {
                "type": "box",
                "layout": "baseline",
                "margin": "md",
                "contents": [
                
            {
                "type": "text",
                "text": "HP :"+str(now_hp)+"/"+str(monster_json["hp"]),
                "align": "center",
                "weight": "bold"
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
                        "text": "介紹",
                        "color": "#aaaaaa",
                        "size": "sm",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": "先填空還沒想到...",
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
                        "text": "攻擊力",
                        "color": "#aaaaaa",
                        "size": "sm",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": str(monster_json["attack"]),
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
                "style": "primary",
                "height": "sm",
                "action": {
                "type": "message",
                "label": "攻擊",
                "text": "@attack"
                }
            },
            {
                "type": "button",
                "style": "primary",
                "height": "sm",
                "action": {
                "type": "message",
                "label": "逃跑",
                "text": "@run"
                },
                "color": "#ff1a1a"
            }
            ],
            "flex": 0
        }
        }
    return json

def getAttackButton(_totaldamage,_diceResult):
    json = {
    "type": "carousel",
    "contents": [
        {
        "type": "bubble",
        "size": "micro",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "image",
                "url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQB4jbFeg7PyLS7I7RQhww-OjfeuYa3PznaNg&usqp=CAU",
                "size": "sm",
                "aspectMode": "fit",
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
                        "text": "DMG "+str(_totaldamage),
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
                        "text": "骰:"+str(_diceResult)+"* 職業攻擊係數",
                        "color": "#ebebeb",
                        "size": "sm",
                        "flex": 0
                    }
                    ],
                    "spacing": "lg"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "button",
                        "action": {
                        "type": "message",
                        "label": "攻擊",
                        "text": "@attack"
                        },
                        "style": "primary",
                        "height": "sm"
                    }
                    ],
                    "spacing": "sm",
                    "borderColor": "#ffffff",
                    "margin": "xxl",
                    "height": "90px"
                }
                ],
                "position": "relative",
                "offsetBottom": "0px",
                "offsetStart": "0px",
                "offsetEnd": "0px",
                "backgroundColor": "#03303Acc",
                "height": "150px",
                "paddingAll": "20px"
            }
            ],
            "paddingAll": "0px"
        }
        }
    ]
    }
    return json


def getBattleEnd(game_result_json):
    json = {
    "type": "carousel",
    "contents": [
        {
        "type": "bubble",
        "size": "nano",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "戰鬥勝利!",
                "color": "#ffffff",
                "align": "start",
                "size": "md",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": " ",
                "color": "#ffffff",
                "align": "start",
                "size": "xs",
                "gravity": "center",
                "margin": "lg"
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
                "type": "text",
                "text": "勇敢的冒險者:",
                "color": "#8C8C8C",
                "size": "sm",
                "wrap": True
            },
            {
                "type": "text",
                "text": "是否要再去冒險呢",
                "color": "#8C8C8C",
                "size": "sm",
                "wrap": True
            },
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "繼續探索",
                "text": "@exper"
                }
            }
            ],
            "spacing": "none",
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
        "size": "nano",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "獲得經驗",
                "color": "#ffffff",
                "align": "start",
                "size": "md",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": str(game_result_json["monster_result_json"]["exp"]),
                "color": "#ffffff",
                "align": "start",
                "size": "xs",
                "gravity": "center",
                "margin": "lg"
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
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "隨時確認狀態",
                    "color": "#8C8C8C",
                    "size": "sm",
                    "wrap": True
                },
                {
                    "type": "text",
                    "color": "#8C8C8C",
                    "size": "sm",
                    "wrap": True,
                    "text": "累了就休息吧"
                },
                {
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "查看狀態",
                    "text": "@jobinfo"
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
        "size": "nano",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "戰利品",
                "color": "#ffffff",
                "align": "start",
                "size": "md",
                "gravity": "center"
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
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "道具系統開發中...敬請期待",
                    "color": "#8C8C8C",
                    "size": "sm",
                    "wrap": True
                },
                {
                    "type": "text",
                    "text": " ",
                    "color": "#8C8C8C",
                    "size": "sm",
                    "wrap": True
                },
                {
                    "type": "text",
                    "text": "花費: $ 10000",
                    "size": "xs"
                },
                {
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "回復狀態",
                    "text": "@health"
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