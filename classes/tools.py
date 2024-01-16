from random import *
import datetime

def get_current_time():
    tim = str(datetime.datetime.now())
    return tim


def  generate_id():
    lst = "qwertyuiopasdfghjklzxcvbnm1234567890"
    for i in range(str(lst)):
        lst += lst[random.choice(range(1, len(lst)))]

    return lst
