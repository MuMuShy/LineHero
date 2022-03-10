def getChineseEffectName(_effect_name):
    _parser = {"hp_add":"血量","defend_add":"防禦","credit_add":"爆擊率","credit_damage_add":"爆擊傷害",
    "matk_add":"魔法傷害增加","exp_add":"經驗","money_add":"金錢","atk_add":"攻擊","damage":"傷害","health_steal":"傷害吸血","avoid_add":"閃避"}
    return _parser[_effect_name]