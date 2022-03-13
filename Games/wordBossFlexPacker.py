from datetime import datetime, timedelta
def getWordBossInfo(word_boss_status,user_word_status,word_boss_basic_info):
    _url = word_boss_basic_info["boss_image_url"]
    _bossname = word_boss_basic_info["boss_name"]
    _starttime = word_boss_status["start_time"]
    _starttime = datetime.strptime(_starttime,"%m/%d/%Y %H:%M:%S")
    _endtime = _starttime+timedelta(days=7)
    _endtime = _endtime.strftime("%m/%d/%Y")
    _nowhp = word_boss_status["hp"]
    _maxhp = word_boss_basic_info["boss_hp"]
    _percent = (_nowhp/_maxhp)*100
    drop_weapon = word_boss_basic_info["boss_drop_weapon"]
    # _weaponurl = "https://mumu.tw/images/weapons/"+str(drop_weapon[0])+".jpg"
    # _weaponurl2 = "https://mumu.tw/images/weapons/"+str(drop_weapon[1])+".jpg"
    # _weaponurl3 = "https://mumu.tw/images/weapons/"+str(drop_weapon[2])+".jpg"
    top5str= []
    for i in range(5):
        try:
            user = user_word_status[i]
        except:
            user = {"player_name":"無","word_guide":-1,"total_damage":0}
        guide = user["word_guide"]
        if guide == 1:
            guide = "瓦倫艾爾"
        elif guide == 2:
            guide = "阿斯拉"
        elif guide ==3:
            guide = "荷拉薇亞"
        else:
            guide = "無陣營"
        top5str.append(user["player_name"]+" 陣營:"+guide+" Damage:"+str(user["total_damage"]))
    json = {
    "type": "carousel",
    "contents": [
        {
        "type": "bubble",
        "size": "giga",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "image",
                "url": _url,
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
                        "text": _bossname,
                        "size": "xl",
                        "color": "#ffffff",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": "擊殺期限 : "+_endtime,
                        "color": "#ffffff"
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
                        "contents": [],
                        "width": str(_percent)+"%",
                        "height": "6px",
                        "backgroundColor": "#E91010"
                    }
                    ],
                    "height": "6px",
                    "backgroundColor": "#9FD8E36E"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                    {
                        "type": "text",
                        "text": "HP : ",
                        "color": "#ebebeb",
                        "size": "sm",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": str(_nowhp),
                        "color": "#ffffffcc",
                        "gravity": "bottom",
                        "flex": 0,
                        "size": "sm"
                    },
                    {
                        "type": "text",
                        "text": "/",
                        "color": "#FFFFFF",
                        "gravity": "bottom",
                        "flex": 0,
                        "size": "sm"
                    },
                    {
                        "type": "text",
                        "text": str(_maxhp),
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
                            "url": "https://mumu.tw/images/menu_icons/25.png"
                        },
                        {
                            "type": "text",
                            "text": "攻擊",
                            "color": "#ffffff",
                            "flex": 0,
                            "offsetTop": "-2px",
                            "action": {
                            "type": "message",
                            "label": "攻擊",
                            "text": "@attackWordBoss"
                            }
                        },
                        {
                            "type": "filler"
                        }
                        ],
                        "spacing": "sm"
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
                    "height": "40px",
                    "action": {
                    "type": "message",
                    "label": "攻擊",
                    "text": "@attackWordBoss"
                    }
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
                    "text": "世界Boss",
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
                "width": "106px"
            }
            ],
            "paddingAll": "0px"
        }
        },
        {
        "type": "bubble",
        "size": "giga",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "image",
                "url": "https://preview.redd.it/mmyi6cyu7od21.jpg?auto=webp&s=999ae9d2505757a14f210e4400102436c7861e1c",
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
                        "text": "傷害排行",
                        "size": "xl",
                        "color": "#ffffff",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": "最高陣營會額外獲得獎勵",
                        "size": "lg",
                        "color": "#ffffff",
                        "weight": "bold"
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
                            "text": top5str[0],
                            "color": "#ebebeb",
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
                            "text": top5str[1],
                            "color": "#ebebeb",
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
                            "text": top5str[2],
                            "color": "#ebebeb",
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
                            "text": top5str[3],
                            "color": "#ebebeb",
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
                            "text": top5str[4],
                            "color": "#ebebeb",
                            "size": "sm",
                            "flex": 0
                        }
                        ],
                        "spacing": "lg"
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "特殊掉落物",
                        "size": "xl",
                        "color": "#ffffff",
                        "weight": "bold",
                        "align": "center",
                        "offsetTop": "5px"
                    }
                    ],
                    "borderWidth": "1px",
                    "cornerRadius": "4px",
                    "spacing": "sm",
                    "borderColor": "#ffffff",
                    "margin": "xxl",
                    "height": "40px",
                    "action": {
                    "type": "message",
                    "label": "攻擊",
                    "text": "@attackWordBoss"
                    }
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
                            "url": "https://i.pinimg.com/originals/ab/a5/13/aba513379a6584623b6a1a765cc17172.jpg",
                            "size": "full",
                            "aspectMode": "fit"
                        },
                        {
                            "type": "text",
                            "text": "神棄之書",
                            "color": "#ffffff",
                            "align": "center"
                        }
                        ],
                        "spacing": "xs"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "image",
                            "url": "https://s3.envato.com/files/281174196/_01.jpg",
                            "size": "full",
                            "aspectMode": "fit"
                        },
                        {
                            "type": "text",
                            "text": "弒龍王者",
                            "color": "#ffffff",
                            "align": "center"
                        }
                        ],
                        "spacing": "xs"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "image",
                            "url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSdwPJ_qnwcG61ZtSnrq4P-eISX-OWOpesntw&usqp=CAU",
                            "size": "full",
                            "aspectMode": "fit"
                        },
                        {
                            "type": "text",
                            "text": "試煉之匕",
                            "color": "#ffffff",
                            "align": "center"
                        }
                        ],
                        "spacing": "xs"
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "世界Boss規則",
                        "size": "xl",
                        "color": "#ffffff",
                        "weight": "bold",
                        "align": "center"
                    }
                    ],
                    "borderWidth": "1px",
                    "cornerRadius": "4px",
                    "spacing": "sm",
                    "borderColor": "#ffffff",
                    "margin": "xxl",
                    "height": "30px"
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
                            "text": "整體傷害所占比例越高獲得獎勵機會越高",
                            "color": "#ffffff",
                            "size": "xxs",
                            "maxLines": 5
                        },
                        {
                            "type": "text",
                            "text": "陣營累積傷害最高將會獲得陣營資源",
                            "color": "#ffffff",
                            "size": "xxs",
                            "maxLines": 5
                        },
                        {
                            "type": "text",
                            "text": "只要有參與擊殺皆有機會獲得獎勵",
                            "color": "#ffffff",
                            "size": "xxs",
                            "maxLines": 5
                        }
                        ],
                        "height": "50px"
                    },
                    {
                        "type": "separator",
                        "margin": "md",
                        "color": "#ffffff"
                    }
                    ]
                }
                ],
                "position": "absolute",
                "offsetBottom": "0px",
                "offsetStart": "0px",
                "offsetEnd": "0px",
                "backgroundColor": "#03303Acc",
                "paddingAll": "20px",
                "paddingTop": "18px"
            }
            ],
            "paddingAll": "0px"
        }
        }
    ]
    }
    return json