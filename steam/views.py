import time

import RPi.GPIO as GPIO
from asgiref.sync import sync_to_async
from mfrc522 import SimpleMFRC522
from steam.models import *
from luma.core.interface.serial import spi, noop
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, LCD_FONT, CP437_FONT, TINY_FONT, DEFAULT_FONT
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.led_matrix.device import max7219

# Create your views here.
reader = SimpleMFRC522()
GPIO.setwarnings(False)

import json
import asyncio

from django.http import HttpResponse
from django.shortcuts import render

from threading import Thread
from datetime import datetime

#
class ProcessThread(Thread, ):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
        self.started = datetime.now()

    def run(self):
        # I added this so you might know how long the process lasted
        # just incase any optimization of your code is needed
        authenticate_user(self.name)
        # finished = datetime.now()
        # duration = self.started - finished
        # print("%s thread started at %s and finished at %s in " \
        #       "%s seconds" % (self.name, self.started, finished, duration))



def ajax_view(request):
    print('Running RFID')
    reader = SimpleMFRC522()
    username = ""
    try:
        id, text = reader.read()
        print(id)
        print(text)
        username = text
        card_id = id
        request.session['username'] = username
        request.session['id'] = card_id
        my_thread = ProcessThread(username)
        my_thread.start()
    finally:
        GPIO.cleanup()

    context = {
        "gebruikersnaam": username,
        "card_id": card_id
    }

    data = json.dumps(context)

    print(f'Returning info: {data}')

    return HttpResponse(data, content_type='application/json')

# helper funcs
def authenticate_user(username):
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, width=32, height=8, block_orientation=-90, cascaded=4)
    device.contrast(5)
    device.clear()
    virtual = viewport(device, width=32, height=8)
    show_message(device, f'Hello {username}', fill="white", font=proportional(LCD_FONT), scroll_delay=0.1)

def index(request):
    # let us now run start the thread
    # print(result)
    return render(request, 'index.html')

def homepage(request):

    username = request.session['username']
    id = request.session['id']


    return render(request, 'home.html', {
        'username': username,
        'id': id
    })