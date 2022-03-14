def getWordGuideStatusList(_wordlist,_kinglist,word_level_list):
    _word1 = _wordlist[0]
    if _word1["word_id"] == 1:
        url1 = "https://mumu.tw/images/npc/valen.png"
    elif _word1["word_id"] ==2:
        url1 = "https://mumu.tw/images/npc/asla.png"
    else:
        url1 = "https://mumu.tw/images/npc/hela.png"
    _word2 = _wordlist[1]
    if _word2["word_id"] == 1:
        url2 = "https://mumu.tw/images/npc/valen.png"
    elif _word2["word_id"] ==2:
        url2 = "https://mumu.tw/images/npc/asla.png"
    else:
        url2 = "https://mumu.tw/images/npc/hela.png"
    _word3 = _wordlist[2]
    if _word3["word_id"] == 1:
        url3 = "https://mumu.tw/images/npc/valen.png"
    elif _word3["word_id"] ==2:
        url3 = "https://mumu.tw/images/npc/asla.png"
    else:
        url3 = "https://mumu.tw/images/npc/hela.png"
    
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
                "url": url1,
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
                        "text": "1. "+_word1["word_name"],
                        "size": "xl",
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
                        "type": "text",
                        "text": "守護神 - "+_word1["word_god"],
                        "color": "#ebebeb",
                        "size": "sm",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": "國王 - "+_kinglist[0],
                        "color": "#ebebeb",
                        "size": "sm",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": "勢力等級 : "+str(_word1["word_level"]),
                        "color": "#ebebeb",
                        "size": "sm",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": "國家財力: "+str(_word1["word_money"]),
                        "color": "#ebebeb",
                        "size": "sm",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": "軍力 : "+str(word_level_list[0]["army_num"]),
                        "color": "#ebebeb",
                        "size": "sm",
                        "flex": 0
                    }
                    ],
                    "spacing": "lg"
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
        },
        {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "image",
                "url": url2,
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
                        "text": "2. "+_word2["word_name"],
                        "size": "xl",
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
                        "type": "text",
                        "text": "守護神 - "+_word2["word_god"],
                        "color": "#ebebeb",
                        "size": "sm",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": "國王 - "+_kinglist[1],
                        "color": "#ebebeb",
                        "size": "sm",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": "勢力等級 : "+str(_word2["word_level"]),
                        "color": "#ebebeb",
                        "size": "sm",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": "國家財力: "+str(_word2["word_money"]),
                        "color": "#ebebeb",
                        "size": "sm",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": "軍力 : "+str(word_level_list[1]["army_num"]),
                        "color": "#ebebeb",
                        "size": "sm",
                        "flex": 0
                    }
                    ],
                    "spacing": "lg"
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
        },
        {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "image",
                "url": url3,
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
                        "text": "3. "+_word3["word_name"],
                        "size": "xl",
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
                        "type": "text",
                        "text": "守護神 - "+_word3["word_god"],
                        "color": "#ebebeb",
                        "size": "sm",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": "國王 - "+_kinglist[2],
                        "color": "#ebebeb",
                        "size": "sm",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": "勢力等級 : "+str(_word3["word_level"]),
                        "color": "#ebebeb",
                        "size": "sm",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": "國家財力: "+str(_word3["word_money"]),
                        "color": "#ebebeb",
                        "size": "sm",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": "軍力 : "+str(word_level_list[2]["army_num"]),
                        "color": "#ebebeb",
                        "size": "sm",
                        "flex": 0
                    }
                    ],
                    "spacing": "lg"
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