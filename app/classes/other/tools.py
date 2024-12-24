from random import *
from datetime import *
import hashlib

from app.classes.other.settings import *

sample = '1h9K8L9h5d5v5Z4q7'


def allowed_file(filename):
    # function of checking file
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_token(s1: str = "vassal228", s2: str = "12345"):
    token = hashlib.sha256(s1.encode() + s2.encode()).hexdigest()
    return token


def get_current_time():
    return str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def generate_id():
    lst = "qwertyuiopasdfghjklzxcvbnm1234567890"
    result = ""
    for _ in range(len(lst)):
        result += lst[choice(range(1, len(lst)))]

    return result
