import os
import eel
from news_shorts import *

eel.init('www')    
os.system('start chrome.exe --app="http://localhost:8000/index.html"')
eel.start('index.html', mode=None, host='localhost', block=True, size=(1920, 1080))