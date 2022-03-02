
import json
from re import L

from Games import rpgDictionary, rpgGame


def getJobInfo(user_img_link,user_job_info,_rank,equipment_weapon_info):
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
                        "text": "STR :"+str(user_job_info["str"])+"+("+str(equipment_weapon_info["str_add"])+")"+"/ INT"+str(user_job_info["int"])+"+("+str(equipment_weapon_info["int_add"])+")"+"/ DEX"+str(user_job_info["dex"])+"+("+str(equipment_weapon_info["dex_add"])+")",
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
                "text": "妖精密林",
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
                    "text": "妖精戰士",
                    "color": "#8C8C8C",
                    "size": "sm",
                    "wrap": True
                },
                {
                    "type": "text",
                    "text": "妖精法師",
                    "color": "#8C8C8C",
                    "size": "sm",
                    "wrap": True
                },
                {
                    "type": "text",
                    "text": "妖精使者",
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
                "text": "@goto elfforest"
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
                "text": "蠻族部落",
                "color": "#ffffff",
                "align": "start",
                "size": "md",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": "推薦LV: 20-30",
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
                    "width": "50%",
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
                    "text": "蠻族守護者",
                    "color": "#8C8C8C",
                    "size": "sm",
                    "wrap": True
                },
                {
                    "type": "text",
                    "text": "蠻族長老",
                    "color": "#8C8C8C",
                    "size": "sm",
                    "wrap": True
                },
                {
                    "type": "text",
                    "text": "依塔洛斯",
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
                "text": "@goto barbarian"
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
        },{
        "type": "bubble",
        "size": "nano",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "百鬼夜行",
                "color": "#ffffff",
                "align": "start",
                "size": "md",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": "推薦LV: 40-50",
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
                    "width": "80%",
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
                    "text": "夜魔",
                    "color": "#8C8C8C",
                    "size": "sm",
                    "wrap": True
                },
                {
                    "type": "text",
                    "text": "鬼魂錢德",
                    "color": "#8C8C8C",
                    "size": "sm",
                    "wrap": True
                },
                {
                    "type": "text",
                    "text": "豔姬",
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
                "text": "@goto ghostroad"
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
    _image_type = monster_json["image_type"]
    _url = "https://mumu.tw/images/monstersimg/"+str(monster_json["monster_id"])+"."+str(_image_type)
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
            },
            "animated": True
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
                        "text": monster_json["description"],
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
        },
        }
    return json

def getAttackButton(_totaldamage,_gameResult):
    #戰士 -> 一顆骰子 結果 4-6
    #法師 ->　兩顆骰子　結果　1-4
    #盜賊 ->三顆骰子　結果1-4
    _dicenum = 0
    _diceresult = _gameResult["dice_result"]
    _iscredit = "未爆擊"
    
    _color_credit = "#b30000"
    _color = "#ffffff"
    job = _gameResult["player_result_json"]["job"]
    if _gameResult["is_credit"] == True:
        _iscredit = "爆擊!"
        _color = _color_credit
    if job =="warrior":
        _dicenum = 1
    elif job =="rog":
        _dicenum = 3
    else:
        _dicenum = 2

    _weapon = _gameResult["player_result_json"]["weapon"]
    _weapon_url = 'https://mumu.tw/images/weapons/'+str(_weapon)+".png"
    if _weapon == 3:
        _weapon_url = 'https://mumu.tw/images/weapons/'+str(_weapon)+".jpg"
    json = {
    "type": "carousel",
    "contents": [
        {
        "type": "bubble",
        "size": "micro",
        "hero": {
            "type": "image",
            "url": "https://mumu.tw/images/menu_icons/1.png",
            "size": "full",
            "align": "center"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "總傷害",
                "weight": "bold",
                "size": "lg",
                "align": "center",
                "color":"#ffffff"
            },
            {
                "type": "text",
                "text": str(_totaldamage),
                "weight": "bold",
                "size": "lg",
                "align": "center",
                "color":_color
            }
            ],
            "paddingAll": "0px",
            "offsetTop": "5px"
        },
        "footer": {
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
                "offsetTop": "8%",
                "height": "sm"
            }
            ],
        "backgroundColor": "#1f1f2e"
        },
        "styles": {
            "hero": {
            "backgroundColor": "#1f1f2e"
            },
            "body": {
            "backgroundColor": "#1f1f2e"
            }
        }
        },
        {
        "type": "bubble",
        "size": "micro",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "可擲骰子 : "+str(_dicenum),
                "weight": "bold",
                "size": "lg",
                "align": "center",
                "color": "#ffffff"
            },
            {
                "type": "text",
                "text": "擲骰結果 : "+str(_gameResult["dice_result"]),
                "weight": "bold",
                "size": "lg",
                "align": "center",
                "color": "#ffffff"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": _iscredit,
                    "align": "center",
                    "size": "xxl",
                    "color": "#ff0000",
                    "weight": "bold",
                    "offsetTop": "50%"
                }
                ],
                "height": "100px"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "傷害加總公式:",
                    "size": "xxs",
                    "color": "#ffffff"
                },
                {
                    "type": "text",
                    "text": "擲骰結果*基本數值係數",
                    "size": "xxs",
                    "weight": "bold",
                    "style": "italic",
                    "color": "#ffffff"
                },
                {
                    "type": "text",
                    "text": "+武器數值*武器係數",
                    "size": "xxs",
                    "weight": "bold",
                    "style": "italic",
                    "color": "#ffffff"
                }
                ],
                "height": "80px",
                "paddingAll": "10%"
            }
            ],
            "paddingAll": "0px",
            "offsetTop": "20px"
        },
        "styles": {
            "hero": {
            "backgroundColor": "#000000"
            },
            "body": {
            "backgroundColor": "#1f1f2e"
            }
        }
        },
    {
      "type": "bubble",
      "size": "micro",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "裝備武器",
            "weight": "bold",
            "size": "lg",
            "align": "center",
            "color": "#ffffff"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "image",
                "url": _weapon_url,
                "size": "xl"
              }
            ],
            "height": "120px"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "武器係數會進入傷害加總的進一步運算",
                "size": "xxs",
                "color": "#ffffff"
              }
            ],
            "height": "80px",
            "paddingAll": "10%"
          }
        ],
        "paddingAll": "0px",
        "offsetTop": "20px"
      },
      "styles": {
        "hero": {
          "backgroundColor": "#000000"
        },
        "body": {
          "backgroundColor": "#1f1f2e"
        }
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
                    "text": "花費:$1500",
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

#裝備欄 技能選單... 等等
def getJobInfoSubMenu():
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
                "text": "裝備欄",
                "color": "#ffffff",
                "align": "start",
                "size": "md",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": "設定裝備物品",
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
                "type": "button",
                "action": {
                "type": "message",
                "label": "裝備",
                "text": "@equipment"
                },
                "style": "primary",
                "margin": "md",
                "height": "sm"
            }
            ],
            "borderWidth": "2px",
            "height": "55px"
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
                "text": "技能列表",
                "color": "#ffffff",
                "align": "start",
                "size": "md",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": "查看&升級技能",
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
                "type": "button",
                "action": {
                "type": "message",
                "label": "技能",
                "text": "@skill"
                },
                "style": "primary",
                "margin": "md",
                "height": "sm"
            }
            ],
            "borderWidth": "2px",
            "height": "55px"
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
                "text": "寵物",
                "color": "#ffffff",
                "align": "start",
                "size": "md",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": "派遣寵物去探險",
                "color": "#ffffff",
                "align": "start",
                "size": "xs",
                "gravity": "center",
                "margin": "lg"
            }
            ],
            "backgroundColor": "#a64dff",
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
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "寵物",
                    "text": "@pet"
                    },
                    "style": "primary",
                    "margin": "md",
                    "height": "sm"
                }
                ],
                "borderWidth": "2px",
                "height": "55px"
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
                "text": "背包",
                "color": "#ffffff",
                "align": "start",
                "size": "md",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": "查看&使用道具",
                "color": "#ffffff",
                "align": "start",
                "size": "xs",
                "gravity": "center",
                "margin": "lg"
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
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "背包",
                    "text": "@bag"
                    },
                    "style": "primary",
                    "margin": "md",
                    "height": "sm"
                }
                ],
                "borderWidth": "2px",
                "height": "55px"
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

def getEquipmentNow(weapon_json):
    from Games import rpgDictionary
    url = "https://mumu.tw/images/weapons/"+str(weapon_json["weapon_id"])+"."+weapon_json["img_type"]
    _start_list =["https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png",
    "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png",
    "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png",
    "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png",
    "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"]
    _rare = int(weapon_json["rare"])-1
    _star = 0
    for i in range(0,_rare):
        _start_list[i] = "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
        _star+=1
    contents = [
                    {
                        "type": "text",
                        "text": "STR + "+str(weapon_json["str_add"]),
                        "wrap": True,
                        "color": "#8c8c8c",
                        "size": "xs",
                        "flex": 5
                    },
                    {
                        "type": "text",
                        "text": "DEX + "+str(weapon_json["dex_add"]),
                        "wrap": True,
                        "color": "#8c8c8c",
                        "size": "xs",
                        "flex": 5
                    },
                    {
                        "type": "text",
                        "text": "INT + "+str(weapon_json["int_add"]),
                        "wrap": True,
                        "color": "#8c8c8c",
                        "size": "xs",
                        "flex": 5
                    },
                    {
                        "type": "text",
                        "text": "攻擊力 + "+str(weapon_json["atk_add"]),
                        "wrap": True,
                        "color": "#8c8c8c",
                        "size": "xs",
                        "flex": 5
                    },

    ]
    for i in weapon_json["other_effect"]:
        _effectchinese = rpgDictionary.getChineseEffectName(i)
        print (weapon_json["other_effect"])
        contents.append(
            {
                        "type": "text",
                        "text": _effectchinese+" : +"+str(weapon_json["other_effect"][i]),
                        "wrap": True,
                        "color": "#ff0000",
                        "size": "xs",
                        "flex": 5
            }
        )

    json = {
    "type": "carousel",
    "contents": [
        {
        "type": "bubble",
        "size": "micro",
        "hero": {
            "type": "image",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "320:213",
            "url": url
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": weapon_json["weapon_name"],
                "weight": "bold",
                "size": "sm",
                "wrap": True
            },
            {
                "type": "box",
                "layout": "baseline",
                "contents": [
                {
                    "type": "icon",
                    "size": "xs",
                    "url": _start_list[0]
                },
                {
                    "type": "icon",
                    "size": "xs",
                    "url": _start_list[1]
                },
                {
                    "type": "icon",
                    "size": "xs",
                    "url": _start_list[2]
                },
                {
                    "type": "icon",
                    "size": "xs",
                    "url": _start_list[3]
                },
                {
                    "type": "icon",
                    "size": "xs",
                    "url": _start_list[4]
                },
                {
                    "type": "text",
                    "text": str(_star)+".0",
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
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": contents
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

def getRpgTop5Rank(top5rankarr):
    json = {
    "type": "bubble",
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "image",
            "url": "https://mumu.tw/images/game_ui/ui.png",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "1:1",
            "gravity": "center",
            "animated": True
        },
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
                    "url": "https://mumu.tw/images/game_ui/rank_head.png",
                    "offsetTop": "5px"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "text",
                        "text": "1."+top5rankarr[0],
                        "size": "md",
                        "color": "#ff3333",
                        "align": "center"
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
                        "contents": [
                        {
                            "type": "text",
                            "text": "2."+top5rankarr[1],
                            "color": "#ffffff",
                            "size": "xs",
                            "flex": 0,
                            "align": "center"
                        }
                        ],
                        "flex": 0,
                        "spacing": "xs"
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                        {
                            "type": "text",
                            "text": "3."+top5rankarr[2],
                            "color": "#ffffff",
                            "size": "xs",
                            "flex": 0,
                            "align": "center"
                        }
                        ],
                        "flex": 0,
                        "spacing": "sm"
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                        {
                            "type": "text",
                            "text": "4."+top5rankarr[3],
                            "color": "#ffffff",
                            "size": "xs",
                            "flex": 0,
                            "align": "center"
                        }
                        ],
                        "flex": 0,
                        "spacing": "sm"
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                        {
                            "type": "text",
                            "text": "5."+top5rankarr[4],
                            "color": "#ffffff",
                            "size": "xs",
                            "flex": 0,
                            "align": "center"
                        }
                        ],
                        "flex": 0,
                        "spacing": "lg"
                    }
                    ],
                    "paddingBottom": "2%"
                }
                ],
                "spacing": "xs"
            }
            ],
            "position": "absolute",
            "offsetBottom": "24%",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px"
        }
        ],
        "paddingAll": "0px",
        "background": {
        "type": "linearGradient",
        "angle": "0deg",
        "startColor": "#000000",
        "endColor": "#ffffff"
        }
    }
    }
    return json

def getSkillList(_player_job_json):
    _description = "戰鬥勝利後 回復10%最大生命值"
    _skillname = "戰士精神"
    skill = "1.png"
    if _player_job_json["job"] == "majic":
        skill = "2.jpg"
        _description = "每回合戰鬥 30%機率增加自身INT30%"
        _skillname = "賢者之力"
    elif _player_job_json["job"] == "rog":
        skill = "3.png"
        _description = "攻擊附帶10%傷害吸血"
        _skillname = "嗜血如命"
    json = {
    "type": "carousel",
    "contents": [
        {
        "type": "bubble",
        "size": "micro",
        "hero": {
            "type": "image",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "320:213",
            "url": "https://mumu.tw/images/skill/"+skill
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": _skillname,
                "weight": "bold",
                "color": "#ffffff",
                "size": "sm",
                "wrap": True,
                "align": "center"
            },
            {
                "type": "box",
                "layout": "baseline",
                "contents": [
                {
                    "type": "text",
                    "text": "被動 不可升級",
                    "size": "xs",
                    "color": "#ffffff",
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
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": _description,
                        "wrap": True,
                        "color": "#ffffff",
                        "size": "xs",
                        "flex": 5
                    }
                    ]
                }
                ]
            }
            ],
            "spacing": "sm",
            "paddingAll": "13px"
        },
        "styles": {
            "hero": {
            "backgroundColor": "#142952"
            },
            "body": {
            "backgroundColor": "#142952"
            }
        }
        }
    ]
    }
    return json

#獲得怪物傷害,玩家剩餘血量的結果按鈕
def getRoundMonsterAliveButton(game_result_json):
    _maxhp = rpgGame.getMaxHp(game_result_json["player_result_json"]["job"],game_result_json["player_result_json"]["level"])
    _present = (game_result_json["player_result_json"]["hp"]/_maxhp)*100
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
                "text": "怪物傷害",
                "color": "#ffffff",
                "align": "start",
                "size": "md",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": str(game_result_json["mosnter_damage"]),
                "color": "#ffffff",
                "align": "start",
                "size": "md",
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
                    "color": "#8C8C8C",
                    "size": "xs",
                    "wrap": True,
                    "text": "傷害計算公式:"
                },
                {
                    "type": "text",
                    "color": "#8C8C8C",
                    "size": "xs",
                    "wrap": True,
                    "text": "(怪物基礎傷害*浮動)-玩家防禦"
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
                "text": "補血",
                "color": "#ffffff",
                "align": "start",
                "size": "md",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": "剩餘血量: "+str(game_result_json["player_result_json"]["hp"]),
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
                    "width": str(_present)+"%",
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
                "type": "button",
                "action": {
                "type": "message",
                "label": "$1500",
                "text": "@health"
                },
                "style": "primary"
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

def getEquipmentPet(pet_info_json):
    _start_list =["https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png",
    "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png",
    "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png",
    "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png",
    "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"]
    _rare = int(pet_info_json["rare"])-1
    _star = 0
    for i in range(0,_rare):
        _start_list[i] = "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
        _star+=1
    contents = []
    print(pet_info_json)
    for i in pet_info_json["other_effect"]:
        _str = rpgDictionary.getChineseEffectName(i)+"+"+pet_info_json["other_effect"][i]
        print("123456")
        contents.append(
            {
                        "type": "text",
                        "text": _str,
                        "color": "#ffffff",
                        "size": "md",
                        "flex": 0,
                        "align": "end"
            }
        )

    print(contents)
    
    _filename = str(pet_info_json["pet_id"])+"."+pet_info_json["img_type"]
    json = {
    "type": "bubble",
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "image",
            "url": "https://mumu.tw/images/pets/"+_filename,
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "1:1",
            "gravity": "center"
        },
        {
            "type": "box",
            "layout": "vertical",
            "contents": [],
            "position": "absolute",
            "background": {
            "type": "linearGradient",
            "angle": "0deg",
            "endColor": "#00000000",
            "startColor": "#00000099"
            },
            "width": "100%",
            "height": "40%",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px"
        },
        {
            "type": "box",
            "layout": "horizontal",
            "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "text",
                        "text": pet_info_json["pet_name"],
                        "size": "xl",
                        "color": "#ffffff"
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                    {
                        "type": "icon",
                        "url": _start_list[0]
                    },
                    {
                        "type": "icon",
                        "url": _start_list[1]
                    },
                    {
                        "type": "icon",
                        "url": _start_list[2]
                    },
                    {
                        "type": "icon",
                        "url": _start_list[3]
                    },
                    {
                        "type": "icon",
                        "url": _start_list[4]
                    },
                    {
                        "type": "text",
                        "text": str(_rare)+".0",
                        "color": "#a9a9a9"
                    }
                    ],
                    "spacing": "xs"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": contents,
                        "flex": 0,
                        "spacing": "lg"
                    }
                    ]
                }
                ],
                "spacing": "xs",
                "backgroundColor": "#00000090"
            }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px"
        }
        ],
        "paddingAll": "0px"
    },
    "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "button",
            "action": {
            "type": "message",
            "label": "遠征隊",
            "text": "@pet_adventure"
            },
            "style": "primary"
        }
        ]
    }
    }
    return json


def getAdventureMap():
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
                "text": "幽暗的洞口",
                "color": "#ffffff",
                "align": "start",
                "size": "md",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": "EXP : 50/MIN ",
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
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "其他掉落物:",
                    "color": "#8C8C8C",
                    "size": "sm",
                    "wrap": True
                },
                {
                    "type": "text",
                    "text": "金幣",
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
                "label": "掛機開始",
                "text": "@petadventureGoto hole"
                },
                "margin": "xs",
                "style": "primary"
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
        "size": "nano",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "敬請期待",
                "color": "#ffffff",
                "align": "start",
                "size": "md",
                "gravity": "center"
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
                "contents": [],
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

#遠征隊目前的狀態
def getAdventureNowStatus(pet_info_json,adventure_info_json):
    _filename = str(pet_info_json["pet_id"])+"."+pet_info_json["img_type"]
    json = {
    "type": "bubble",
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "image",
            "url": "https://mumu.tw/images/pets/"+_filename,
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "1:1",
            "gravity": "center"
        },
        {
            "type": "box",
            "layout": "vertical",
            "contents": [],
            "position": "absolute",
            "background": {
            "type": "linearGradient",
            "angle": "0deg",
            "endColor": "#00000000",
            "startColor": "#00000099"
            },
            "width": "100%",
            "height": "40%",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px"
        },
        {
            "type": "box",
            "layout": "horizontal",
            "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "text",
                        "text": "遠征狀態: "+adventure_info_json["map_name"],
                        "size": "xl",
                        "color": "#ffffff"
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                    {
                        "type": "text",
                        "text": "累積分鐘數 : "+str(adventure_info_json["pass_min"])+"min",
                        "color": "#a9a9a9"
                    }
                    ],
                    "spacing": "xs"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                        {
                            "type": "text",
                            "text": "EXP:"+str(adventure_info_json["total_exp"])+"("+str(adventure_info_json["pet_add_exp"])+"寵)",
                            "color": "#ffffff",
                            "size": "md",
                            "flex": 0,
                            "align": "end"
                        },
                        {
                            "type": "text",
                            "text": "累積金錢: "+str(adventure_info_json["total_money"])+"("+str(adventure_info_json["pet_add_money"])+"寵)",
                            "color": "#ffffff",
                            "size": "md",
                            "flex": 0,
                            "align": "end"
                        }
                        ],
                        "flex": 0,
                        "spacing": "lg"
                    }
                    ]
                }
                ],
                "spacing": "xs",
                "backgroundColor": "#00000090"
            }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px"
        }
        ],
        "paddingAll": "0px"
    },
    "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "button",
            "action": {
            "type": "message",
            "label": "招回",
            "text": "@petadventureback"
            },
            "style": "primary"
        }
        ]
    }
    }
    return json