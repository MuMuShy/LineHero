
from importlib.resources import contents
import json
import math
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
        _jobtext="戰士一轉"
        _weponatk = 1+(equipment_weapon_info["atk_add"]/100)*equipment_weapon_info["atk_add"]*1.3
        _atk = ((user_job_info["str"]+equipment_weapon_info["str_add"])*1.3*6)+_weponatk
        _matk = 0
    elif user_job_info['job'] == "majic":
        maxhp = rpgGame.getMaxHp("majic",user_job_info["level"])     
        jobrul = "https://mumu.tw/images/game_icons/icon_itemicon_book_magic.png"
        _jobtext="法師一轉"
        _weponatk = 1+(equipment_weapon_info["atk_add"]/100)*equipment_weapon_info["atk_add"]*1.7
        _atk = 0
        _matk = ((user_job_info["int"]+equipment_weapon_info["int_add"])*1.6*5)+_weponatk
    else:
        maxhp = rpgGame.getMaxHp("rog",user_job_info["level"])   
        jobrul = "https://mumu.tw/images/game_icons/icon_itemicon_arrow.png"
        _jobtext="盜賊一轉"
        _matk = 0
        _weponatk = 1+(equipment_weapon_info["dex_add"]/100)*equipment_weapon_info["dex_add"]*1.5
        _atk = ((user_job_info["dex"]+equipment_weapon_info["dex_add"])*1.7*6)+_weponatk
    #血量增加確認
    try:
        hp_add = equipment_weapon_info["other_effect"]["hp_add"]
        if "%" in hp_add:
            hp_add = int(hp_add.split("%")[0])
            hp_add/=100
            maxhp = maxhp+maxhp*hp_add
        else:
            hp_add = int(hp_add)
            maxhp+=maxhp
    except:
        None 
    _atk = math.ceil(_atk)
    _matk = math.ceil(_matk)
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
        },
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://mumu.tw/images/game_ui/job_bkg.jpg",
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
                    "text": "JOB",
                    "color": "#ffffff",
                    "weight": "bold"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "text",
                        "text": _jobtext,
                        "color": "#a366ff",
                        "size": "sm",
                        "flex": 0
                      }
                    ],
                    "spacing": "lg",
                    "margin": "none",
                    "justifyContent": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "STR ",
                    "color": "#ffffff",
                    "weight": "bold"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "text",
                        "text": str(user_job_info["str"])+"+("+str(equipment_weapon_info["str_add"])+")",
                        "color": "#e60000",
                        "size": "sm",
                        "flex": 0
                      }
                    ],
                    "spacing": "lg",
                    "justifyContent": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "INT",
                    "color": "#ffffff",
                    "weight": "bold"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "text",
                        "text": str(user_job_info["int"])+"+("+str(equipment_weapon_info["int_add"])+")",
                        "color": "#b380ff",
                        "size": "sm",
                        "flex": 0
                      }
                    ],
                    "spacing": "lg",
                    "justifyContent": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "DEX",
                    "color": "#ffffff",
                    "weight": "bold"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "text",
                        "text": str(user_job_info["dex"])+"+("+str(equipment_weapon_info["dex_add"])+")",
                        "color": "#99ebff",
                        "size": "sm",
                        "flex": 0
                      }
                    ],
                    "spacing": "lg",
                    "justifyContent": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "ATK",
                    "color": "#ffffff",
                    "weight": "bold"
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "text",
                        "text": str(_atk),
                        "color": "#ff6666",
                        "size": "sm",
                        "flex": 0,
                        "weight": "bold",
                        "align": "center"
                      }
                    ],
                    "spacing": "xs",
                    "justifyContent": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "MATK",
                    "color": "#ffffff",
                    "weight": "bold"
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "text",
                        "text": str(_matk),
                        "color": "#ff8080",
                        "size": "sm",
                        "flex": 0,
                        "align": "center"
                      }
                    ],
                    "spacing": "xs",
                    "justifyContent": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "DEFEND",
                    "color": "#ffffff",
                    "weight": "bold"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "text",
                        "text": "1000",
                        "color": "#ffffff",
                        "size": "sm",
                        "flex": 0
                      }
                    ],
                    "spacing": "lg",
                    "justifyContent": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "公會",
                    "color": "#ffffff",
                    "weight": "bold"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "text",
                        "text": "未加入(開發中)",
                        "color": "#ffffff",
                        "size": "sm",
                        "flex": 0
                      }
                    ],
                    "spacing": "lg",
                    "justifyContent": "center"
                  }
                ]
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px",
            "paddingTop": "20px",
            "height": "450px",
            "borderWidth": "20px",
            "backgroundColor": "#0d0d0d80"
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
        },{
        "type": "bubble",
        "size": "nano",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "江戶幕府",
                "color": "#ffffff",
                "align": "start",
                "size": "md",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": "推薦LV: 50-70",
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
                    "width": "90%",
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
                    "text": "桃桃子",
                    "color": "#8C8C8C",
                    "size": "sm",
                    "wrap": True
                },
                {
                    "type": "text",
                    "text": "吹雪",
                    "color": "#8C8C8C",
                    "size": "sm",
                    "wrap": True
                },
                {
                    "type": "text",
                    "text": "三尾狐狸",
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
                "text": "@goto shogunate"
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

    _weapon = _gameResult["weapon_info"]["weapon_id"]
    _imgtype = _gameResult["weapon_info"]["img_type"]
    
    print("img type:"+_imgtype)
    _weapon_url = 'https://mumu.tw/images/weapons/'+str(_weapon)+"."+_imgtype

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
        },{
        "type": "bubble",
        "size": "nano",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "橘子村莊(NEW!)",
                "color": "#ffffff",
                "align": "start",
                "size": "md",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": "商人&NPC",
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
                    "label": "逛逛",
                    "text": "@govillage"
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

def getSkillList(_player_skill_list):
    bubbles = []
    for skill in _player_skill_list:
        _url = "https://mumu.tw/images/skill/"+skill["job"]+"/"+str(skill["skill_id"])+"."+skill["image_type"]
        _level = str(skill["_skilllevel"])
        _nowmaxlevel = skill["used_book_time"]*skill["leveladd_one_book"]+skill["max_level"]
        _name = skill["skill_name"]
        _canlevelup = ""
        _levelupbtn = ""
        if skill["max_level"] == 1 and skill["max_book_time"] == 0:
            _canlevelup = "不可升級"
            _levelupbtn = " "
        else:
            _levelupbtn = "@skilllevelup "+skill["job"]+":"+str(skill["skill_id"])
        type = "被動技能"
        if skill["skill_type"] == "active":
            type = "主動技能"
        type+=_canlevelup
        #每等提升資料
        _levelupinfo = " "
        if skill["skill_effect_addlv_description"] != []:
            _levelupinfo = "每等級提升:\n"
            for skilllvupdes in skill["skill_effect_addlv_description"]:
                type = skilllvupdes.split(":")[0]
                _value =  skilllvupdes.split(":")[1]
                type = rpgDictionary.getChineseEffectName(type)
                _levelupinfo+= type+" "+_value
        bubble = {
                "type": "bubble",
                "size": "micro",
                "hero": {
                    "type": "image",
                    "url": _url,
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
                        "text": _name+" LV "+_level+" 最大:"+str(_nowmaxlevel)+"\n可用技能書:"+str(skill["max_book_time"]),
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
                            "text": type,
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
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                            {
                                "type": "text",
                                "text": skill["skill_description"],
                                "wrap": True,
                                "size": "xs",
                                "flex": 5,
                                "weight": "bold"
                            }
                            ],
                            "height": "100px"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "separator",
                                "margin": "sm"
                            },
                            {
                                "type": "text",
                                "text": _levelupinfo,
                                "size": "xxs"
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
                                "label": "升級",
                                "text": _levelupbtn
                                },
                                "style": "primary"
                            }
                            ]
                        }
                        ]
                    }
                ],
                "spacing": "sm",
                "paddingAll": "13px"
            }
            }
        bubbles.append(bubble)
    json = {
    "type": "carousel",
    "contents": bubbles
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

def getEquipmentList(_weapon_json_list,isFirst = True):
    from Games import rpgDictionary
    index = 0 # 0的時候為裝備中道具
    bubble_contents=[]
    for weapon in _weapon_json_list:
        #print("要打包")
        #print(weapon)
        _buttontext = "@changeequipment "+str(weapon["backpack_loc"])
        if isFirst:
            if index == 0:
                _btnstyle = "secondary"
                _btnlabel = "裝備中"
                _buttontext = " "
            else:
                _btnstyle = "primary"
                _btnlabel = "裝備"
        else:
            _btnstyle = "primary"
            _btnlabel = "裝備"
        
        _reel_time = ""
        if weapon["success_time"] > 0:
            _reel_time =" + "+str(weapon["success_time"])
        url = "https://mumu.tw/images/weapons/"+str(weapon["weapon_id"])+"."+weapon["img_type"]
        _start_list =["https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png",
        "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png",
        "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png",
        "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png",
        "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"]
        _rare = int(weapon["rare"])-1
        _star = 0
        for i in range(0,_rare):
            _start_list[i] = "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
            _star+=1
            contents = [
                            {
                                "type": "text",
                                "text": "STR + "+str(weapon["str_add"]),
                                "wrap": True,
                                "color": "#8c8c8c",
                                "size": "xs",
                                "flex": 5
                            },
                            {
                                "type": "text",
                                "text": "DEX + "+str(weapon["dex_add"]),
                                "wrap": True,
                                "color": "#8c8c8c",
                                "size": "xs",
                                "flex": 5
                            },
                            {
                                "type": "text",
                                "text": "INT + "+str(weapon["int_add"]),
                                "wrap": True,
                                "color": "#8c8c8c",
                                "size": "xs",
                                "flex": 5
                            },
                            {
                                "type": "text",
                                "text": "攻擊力 + "+str(weapon["atk_add"]),
                                "wrap": True,
                                "color": "#8c8c8c",
                                "size": "xs",
                                "flex": 5
                            },

            ]
        for i in weapon["other_effect"]:
            _effectchinese = rpgDictionary.getChineseEffectName(i)
            print (weapon["other_effect"])
            contents.append(
                {
                            "type": "text",
                            "text": _effectchinese+" : +"+str(weapon["other_effect"][i]),
                            "wrap": True,
                            "color": "#ff0000",
                            "size": "xs",
                            "flex": 5
                }
            )
        contents.append(
            {
                "type": "text",
                "text": "可使用卷軸次數:"+str(weapon["available_reeltime"]),
                "wrap": True,
                "color": "#000000",
                "size": "xs",
                "flex": 5
            }
        )
        bubbble = {
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
                "text": weapon["weapon_name"]+_reel_time,
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
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                 "type": "button",
                "action": {
                "type": "message",
                "label": _btnlabel,
                "text": _buttontext
                },
                "style": _btnstyle
            }
            ]
        }
        }
        index+=1
        bubble_contents.append(bubbble)
    json = {
    "type": "carousel",
    "contents":bubble_contents
    }
    return json

def getEquipmentSellList(_weapon_json_list,isFirst = True):
    from Games import rpgDictionary
    index = 0 # 0的時候為裝備中道具
    bubble_contents=[]
    for weapon in _weapon_json_list:
        #print("要打包")
        #print(weapon)
        _buttontext = "@sellweapon "+str(weapon["backpack_loc"])
        if isFirst:
            if index == 0:
                _btnstyle = "secondary"
                _btnlabel = "裝備中"
                _buttontext = " "
            else:
                _btnstyle = "primary"
                _btnlabel = "販賣"
        else:
            _btnstyle = "primary"
            _btnlabel = "販賣"
        
        _reel_time = ""
        if weapon["success_time"] > 0:
            _reel_time =" + "+str(weapon["success_time"])
        url = "https://mumu.tw/images/weapons/"+str(weapon["weapon_id"])+"."+weapon["img_type"]
        _start_list =["https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png",
        "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png",
        "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png",
        "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png",
        "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"]
        _rare = int(weapon["rare"])-1
        _star = 0
        for i in range(0,_rare):
            _start_list[i] = "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
            _star+=1
            contents = [
                            {
                                "type": "text",
                                "text": "STR + "+str(weapon["str_add"]),
                                "wrap": True,
                                "color": "#8c8c8c",
                                "size": "xs",
                                "flex": 5
                            },
                            {
                                "type": "text",
                                "text": "DEX + "+str(weapon["dex_add"]),
                                "wrap": True,
                                "color": "#8c8c8c",
                                "size": "xs",
                                "flex": 5
                            },
                            {
                                "type": "text",
                                "text": "INT + "+str(weapon["int_add"]),
                                "wrap": True,
                                "color": "#8c8c8c",
                                "size": "xs",
                                "flex": 5
                            },
                            {
                                "type": "text",
                                "text": "攻擊力 + "+str(weapon["atk_add"]),
                                "wrap": True,
                                "color": "#8c8c8c",
                                "size": "xs",
                                "flex": 5
                            },

            ]
        for i in weapon["other_effect"]:
            _effectchinese = rpgDictionary.getChineseEffectName(i)
            print (weapon["other_effect"])
            contents.append(
                {
                            "type": "text",
                            "text": _effectchinese+" : +"+str(weapon["other_effect"][i]),
                            "wrap": True,
                            "color": "#ff0000",
                            "size": "xs",
                            "flex": 5
                }
            )
        contents.append(
            {
                "type": "text",
                "text": "可使用卷軸次數:"+str(weapon["available_reeltime"]),
                "wrap": True,
                "color": "#000000",
                "size": "xs",
                "flex": 5
            }
        )
        bubbble = {
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
                "text": weapon["weapon_name"]+_reel_time,
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
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                 "type": "button",
                "action": {
                "type": "message",
                "label": _btnlabel,
                "text": _buttontext
                },
                "style": _btnstyle
            }
            ]
        }
        }
        index+=1
        bubble_contents.append(bubbble)
    json = {
    "type": "carousel",
    "contents":bubble_contents
    }
    return json

def getUsefulItemMenu():
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
                "text": "卷軸",
                "color": "#ffffff",
                "align": "start",
                "size": "md",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": "武器/防具強化",
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
                "label": "打開",
                "text": "@showreelList"
                },
                "style": "primary",
                "offsetTop": "5px"
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
                "text": "消耗品",
                "color": "#ffffff",
                "align": "start",
                "size": "md",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": "加成道具",
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
                "label": "打開",
                "text": "@showusefullist"
                },
                "style": "primary",
                "offsetTop": "5px"
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

def getUserReelList(_reels_json):
    _baseurl = "https://mumu.tw/images/reels/"
    _bubbles = []
    for reel in _reels_json:
        _reelinfo = reel["reel_info_json"]
        _reelid = _reelinfo["reel_id"]
        _imgtype = _reelinfo["image_type"]
        _quantity = reel["quantity"]
        _4basicPowercontents = [] #四維屬性加乘
        if _reelinfo["plus_str"] != 0:
            _4basicPowercontents.append(
                {
                        "type": "text",
                        "text": "STR + "+str(_reelinfo["plus_str"]),
                        "wrap": True,
                        "color": "#8c8c8c",
                        "size": "xs",
                        "flex": 5
                }
            )
        if _reelinfo["plus_int"] != 0:
            _4basicPowercontents.append(
                {
                        "type": "text",
                        "text": "INT + "+str(_reelinfo["plus_int"]),
                        "wrap": True,
                        "color": "#8c8c8c",
                        "size": "xs",
                        "flex": 5
                }
            )
        if _reelinfo["plus_dex"] != 0:
            _4basicPowercontents.append(
                {
                        "type": "text",
                        "text": "DEX + "+str(_reelinfo["plus_dex"]),
                        "wrap": True,
                        "color": "#8c8c8c",
                        "size": "xs",
                        "flex": 5
                }
            )
        if _reelinfo["plus_atk"] != 0:
            _4basicPowercontents.append(
                {
                        "type": "text",
                        "text": "ATK + "+str(_reelinfo["plus_atk"]),
                        "wrap": True,
                        "color": "#8c8c8c",
                        "size": "xs",
                        "flex": 5
                }
            )
        _otherDescription=[]
        if _reelinfo["description"] is not None:
            for des in _reelinfo["description"]:
                _type = des.split(":")[0]
                _value = des.split(":")[1]
                _typechinese = rpgDictionary.getChineseEffectName(_type)
                _otherDescription.append(
                        {
                        "type": "text",
                        "text": _typechinese+" + "+str(_value),
                        "size": "xs"
                    }
                )
        _bubble = {
            "type": "bubble",
            "size": "micro",
            "hero": {
                "type": "image",
                "url": _baseurl+str(_reelid)+"."+_imgtype,
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
                    "text": _reelinfo["reel_name"],
                    "weight": "bold",
                    "size": "sm",
                    "wrap": True
                },
                {
                    "type": "text",
                    "text": "持有 : "+str(_quantity),
                    "size": "xxs",
                    "weight": "bold"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents":_4basicPowercontents
                        
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": _otherDescription
                }
                ],
                "spacing": "sm",
                "paddingAll": "13px"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "使用",
                    "text": "@useReel "+str(_reelid)
                    },
                    "style": "primary"
                }
                ]
            }
            }
        _bubbles.append(_bubble)
    json = {
         "type": "carousel",
         "contents":_bubbles
    }
    return json

def getReelSellList(_reels_json):
    _baseurl = "https://mumu.tw/images/reels/"
    _bubbles = []
    for reel in _reels_json:
        _reelinfo = reel["reel_info_json"]
        _reelid = _reelinfo["reel_id"]
        _imgtype = _reelinfo["image_type"]
        _quantity = reel["quantity"]
        _4basicPowercontents = [] #四維屬性加乘
        if _reelinfo["plus_str"] != 0:
            _4basicPowercontents.append(
                {
                        "type": "text",
                        "text": "STR + "+str(_reelinfo["plus_str"]),
                        "wrap": True,
                        "color": "#8c8c8c",
                        "size": "xs",
                        "flex": 5
                }
            )
        if _reelinfo["plus_int"] != 0:
            _4basicPowercontents.append(
                {
                        "type": "text",
                        "text": "INT + "+str(_reelinfo["plus_int"]),
                        "wrap": True,
                        "color": "#8c8c8c",
                        "size": "xs",
                        "flex": 5
                }
            )
        if _reelinfo["plus_dex"] != 0:
            _4basicPowercontents.append(
                {
                        "type": "text",
                        "text": "DEX + "+str(_reelinfo["plus_dex"]),
                        "wrap": True,
                        "color": "#8c8c8c",
                        "size": "xs",
                        "flex": 5
                }
            )
        if _reelinfo["plus_atk"] != 0:
            _4basicPowercontents.append(
                {
                        "type": "text",
                        "text": "ATK + "+str(_reelinfo["plus_atk"]),
                        "wrap": True,
                        "color": "#8c8c8c",
                        "size": "xs",
                        "flex": 5
                }
            )
        _otherDescription=[]
        if _reelinfo["description"] is not None:
            for des in _reelinfo["description"]:
                _type = des.split(":")[0]
                _value = des.split(":")[1]
                _typechinese = rpgDictionary.getChineseEffectName(_type)
                _otherDescription.append(
                        {
                        "type": "text",
                        "text": _typechinese+" + "+str(_value),
                        "size": "xs"
                    }
                )
        _bubble = {
            "type": "bubble",
            "size": "micro",
            "hero": {
                "type": "image",
                "url": _baseurl+str(_reelid)+"."+_imgtype,
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
                    "text": _reelinfo["reel_name"],
                    "weight": "bold",
                    "size": "sm",
                    "wrap": True
                },
                {
                    "type": "text",
                    "text": "持有 : "+str(_quantity),
                    "size": "xxs",
                    "weight": "bold"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents":_4basicPowercontents
                        
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": _otherDescription
                }
                ],
                "spacing": "sm",
                "paddingAll": "13px"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "button",
                    "action": {
                    "type": "message",
                    "label": "販賣",
                    "text": "@sellReel "+str(_reelid)
                    },
                    "style": "primary"
                }
                ]
            }
            }
        _bubbles.append(_bubble)
    json = {
         "type": "carousel",
         "contents":_bubbles
    }
    return json

def getUserActiveSkills(skill_list):
    bubbles = []
    for skill in skill_list:
        _url = "https://mumu.tw/images/skill/"+skill["job"]+"/"+str(skill["skill_id"])+"."+skill["image_type"]
        _name = skill["skill_name"]
        bubble = {
      "type": "bubble",
      "size": "nano",
      "header": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": _url,
            "size": "full"
          }
        ]
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
                "text": _name,
                "size": "sm",
                "wrap": True,
                "weight": "bold",
                "align": "center"
              }
            ],
            "flex": 1
          },
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "使用",
              "text": "@useskill "+skill["job"]+" "+str(skill["skill_id"])
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
    bubbles.append(bubble)
    json =  {
    "type": "carousel",
    "contents": bubbles
    }
    return json

#轉但結果
def getGashsopResult(url,text):
    json = {
    "type": "bubble",
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "image",
            "url": url,
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
                        "text": text,
                        "size": "xl",
                        "color": "#ffffff"
                    }
                    ]
                }
                ],
                "spacing": "xs"
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
    }
    }
    return json

def getVillageMenu():
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
                "text": "村莊商店",
                "color": "#ffffff",
                "align": "start",
                "size": "md",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": "不二價",
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
                "layout": "horizontal",
                "contents": [
                {
                    "type": "text",
                    "text": "提供基礎的裝備,消耗品等資源",
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
                "label": "逛逛",
                "text": "@viewshop"
                },
                "style": "primary",
                "margin": "none"
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
                "text": "鑽石商城",
                "color": "#ffffff",
                "align": "start",
                "size": "md",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": "機率公開公正",
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
                "layout": "horizontal",
                "contents": [
                {
                    "type": "text",
                    "text": "轉蛋機",
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
                "label": "準備中",
                "text": " "
                },
                "style": "secondary",
                "margin": "none"
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



def getShopingMan():
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
                "url": "https://mumu.tw/images/game_ui/shopmen.jpg",
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
                        "text": "遊蕩商人 - 碩寶寶",
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
                        "text": "基本武器,卷軸販賣,往右滑可以逛逛喔~",
                        "color": "#ffffffcc",
                        "gravity": "bottom",
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
                        "type": "filler"
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                        {
                            "type": "filler"
                        },
                        {
                            "type": "icon",
                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/flexsnapshot/clip/clip14.png"
                        },
                        {
                            "type": "text",
                            "color": "#ffffff",
                            "flex": 0,
                            "offsetTop": "-2px",
                            "text": "販賣裝備"
                        },
                        {
                            "type": "filler"
                        }
                        ],
                        "spacing": "sm",
                        "action": {
                        "type": "message",
                        "text": "@sellweapon",
                        "label": " "
                        }
                    },
                    {
                        "type": "filler"
                    }
                    ],
                    "borderWidth": "1px",
                    "cornerRadius": "4px",
                    "spacing": "sm",
                    "borderColor": "#ffffff",
                    "margin": "xxl",
                    "height": "40px"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "filler"
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                        {
                            "type": "filler"
                        },
                        {
                            "type": "icon",
                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/flexsnapshot/clip/clip14.png"
                        },
                        {
                            "type": "text",
                            "color": "#ffffff",
                            "flex": 0,
                            "offsetTop": "-2px",
                            "text": "販賣消耗品"
                        },
                        {
                            "type": "filler",
                        }
                        ],
                        "spacing": "sm",
                        "action": {
                        "type": "message",
                        "label": "action",
                        "text": "@selluseful"
                        }
                    },
                    {
                        "type": "filler"
                    }
                    ],
                    "borderWidth": "1px",
                    "cornerRadius": "4px",
                    "spacing": "sm",
                    "borderColor": "#ffffff",
                    "margin": "xxl",
                    "height": "40px"
                }
                ],
                "position": "absolute",
                "offsetBottom": "0px",
                "offsetStart": "0px",
                "offsetEnd": "0px",
                "backgroundColor": "#03303Acc",
                "paddingAll": "20px",
                "paddingTop": "18px"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "NPC",
                    "color": "#ffffff",
                    "align": "center",
                    "size": "xs",
                    "offsetTop": "3px"
                }
                ],
                "position": "absolute",
                "cornerRadius": "20px",
                "offsetTop": "18px",
                "backgroundColor": "#ff334b",
                "offsetStart": "18px",
                "height": "25px",
                "width": "53px"
            }
            ],
            "paddingAll": "0px"
        }
        },
        {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "image",
                "url": "https://mumu.tw/images/game_ui/shopbg.jpg",
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
                        "text": "武器專區",
                        "size": "xl",
                        "color": "#ffffff",
                        "weight": "bold",
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
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "image",
                            "url": "https://mumu.tw/images/weapons/1.png",
                            "size": "xxs",
                            "align": "start"
                        },
                        {
                            "type": "text",
                            "text": "$ 19999",
                            "offsetTop": "10px",
                            "color": "#ffffff"
                        },
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "購買",
                            "text": "@buyshopweapon 1"
                            },
                            "margin": "none",
                            "style": "primary",
                            "height": "sm"
                        }
                        ],
                        "spacing": "10px",
                        "margin": "0px"
                    },
                    {
                        "type": "text",
                        "text": "劍士裝備 勇者之劍",
                        "color": "#ffffff"
                    }
                    ],
                    "margin": "30px"
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
                            "type": "image",
                            "url": "https://mumu.tw/images/weapons/2.png",
                            "size": "xxs",
                            "align": "start"
                        },
                        {
                            "type": "text",
                            "text": "$ 19999",
                            "offsetTop": "10px",
                            "color": "#ffffff"
                        },
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "購買",
                            "text": "@buyshopweapon 2"
                            },
                            "margin": "none",
                            "style": "primary",
                            "height": "sm"
                        }
                        ],
                        "spacing": "10px",
                        "margin": "0px"
                    },
                    {
                        "type": "text",
                        "text": "盜賊裝備 勇者匕首",
                        "color": "#ffffff"
                    }
                    ],
                    "margin": "30px"
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
                            "type": "image",
                            "url": "https://mumu.tw/images/weapons/3.jpg",
                            "size": "xxs",
                            "align": "start"
                        },
                        {
                            "type": "text",
                            "text": "$ 19999",
                            "offsetTop": "10px",
                            "color": "#ffffff"
                        },
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "購買",
                            "text": "@buyshopweapon 3"
                            },
                            "margin": "none",
                            "style": "primary",
                            "height": "sm"
                        }
                        ],
                        "spacing": "10px",
                        "margin": "0px"
                    },
                    {
                        "type": "text",
                        "text": "法師裝備 勇者之書",
                        "color": "#ffffff"
                    }
                    ],
                    "margin": "30px"
                }
                ],
                "position": "absolute",
                "offsetBottom": "0px",
                "offsetStart": "0px",
                "offsetEnd": "0px",
                "backgroundColor": "#13060680",
                "paddingAll": "20px",
                "paddingTop": "18px",
                "offsetTop": "-5px"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "SALE",
                    "color": "#ffffff",
                    "align": "center",
                    "size": "xs",
                    "offsetTop": "3px"
                }
                ],
                "position": "absolute",
                "cornerRadius": "20px",
                "offsetTop": "18px",
                "backgroundColor": "#ff334b",
                "offsetStart": "18px",
                "height": "25px",
                "width": "53px"
            }
            ],
            "paddingAll": "0px"
        }
        },
        {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "image",
                "url": "https://mumu.tw/images/game_ui/shopbg.jpg",
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
                        "text": "卷軸專區",
                        "size": "xl",
                        "color": "#ffffff",
                        "weight": "bold",
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
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "image",
                            "url": "https://mumu.tw/images/reels/1.jpg",
                            "size": "xxs",
                            "align": "start"
                        },
                        {
                            "type": "text",
                            "text": "$ 10000",
                            "offsetTop": "10px",
                            "color": "#ffffff"
                        },
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "購買",
                            "text": "@buyshopreel 1"
                            },
                            "margin": "none",
                            "style": "primary",
                            "height": "sm"
                        }
                        ],
                        "spacing": "10px",
                        "margin": "0px"
                    },
                    {
                        "type": "text",
                        "text": "100% 攻擊力卷軸",
                        "color": "#ffffff"
                    }
                    ],
                    "margin": "30px"
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
                            "type": "image",
                            "url": "https://mumu.tw/images/reels/3.jpg",
                            "size": "xxs",
                            "align": "start"
                        },
                        {
                            "type": "text",
                            "text": "$ 10000",
                            "offsetTop": "10px",
                            "color": "#ffffff"
                        },
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "購買",
                            "text": "@buyshopreel 3"
                            },
                            "margin": "none",
                            "style": "primary",
                            "height": "sm"
                        }
                        ],
                        "spacing": "10px",
                        "margin": "0px"
                    },
                    {
                        "type": "text",
                        "text": "100% 屬性卷軸",
                        "color": "#ffffff"
                    }
                    ],
                    "margin": "30px"
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
                            "type": "image",
                            "url": "https://mumu.tw/images/reels/5.jpg",
                            "size": "xxs",
                            "align": "start"
                        },
                        {
                            "type": "text",
                            "text": "$ 10000",
                            "offsetTop": "10px",
                            "color": "#ffffff"
                        },
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "購買",
                            "text": "@buyshopreel 5"
                            },
                            "margin": "none",
                            "style": "primary",
                            "height": "sm"
                        }
                        ],
                        "spacing": "10px",
                        "margin": "0px"
                    },
                    {
                        "type": "text",
                        "text": "100% 爆擊卷軸",
                        "color": "#ffffff"
                    }
                    ],
                    "margin": "30px"
                }
                ],
                "position": "absolute",
                "offsetBottom": "0px",
                "offsetStart": "0px",
                "offsetEnd": "0px",
                "backgroundColor": "#13060680",
                "paddingAll": "20px",
                "paddingTop": "18px",
                "offsetTop": "-5px"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "SALE",
                    "color": "#ffffff",
                    "align": "center",
                    "size": "xs",
                    "offsetTop": "3px"
                }
                ],
                "position": "absolute",
                "cornerRadius": "20px",
                "offsetTop": "18px",
                "backgroundColor": "#ff334b",
                "offsetStart": "18px",
                "height": "25px",
                "width": "53px"
            }
            ],
            "paddingAll": "0px"
        }
        }
    ]
    }
    return json