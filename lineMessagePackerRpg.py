
def getJobInfo(user_img_link,user_job_info):
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
                            "text": _jobchinese,
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
                    "text": "LV: 1",
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