import codecs
from datetime import datetime


def get_psw_config():
    output = {}
    with codecs.open('psw.cfg', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for _line in lines:
        line = _line.strip()
        key = line.split('=')[0]
        value = line.split('=')[1]
        output[key] = value
    return output

def meal_time_trans(time):
    """判斷用段為何
    meal_seq = 1  午餐
    meal_seq = 3  下午茶
    meal_seq = 4  晚餐
    """
    hour = time.split(':')[0]
    if int(hour) <= 12:
        return 1, 'lunch'
    elif int(hour) <= 17:
        return 3, 
    elif int(hour) <= 20:
        return 4, 
    