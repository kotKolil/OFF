# External libraries
import requests as r
import sys

# Adding classes to path
sys.path.append('..')

# Importing local classes
from config import *

def test_TestingPageNotFound():
    #testing 404 error
    assert r.get(f"http://{APPhost}:{APPport}/some-adress").status_code == 200


