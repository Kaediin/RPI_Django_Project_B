import time
import json
import asyncio

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from threading import Thread
from datetime import datetime
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

GPIO.setwarnings(False)


class ProcessThread(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
        self.started = datetime.now()

    def run(self):
        print("Show matrix on different thread")
        show_matrix(f'Hello {self.name}')



def ajax_view(request):
    print('Running RFID')
    reader = SimpleMFRC522()
    try:
        id, text = reader.read()
        username = text
        card_id = id
        print(f'User: {username}\nId: {id}')
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

    return HttpResponse(data, content_type='application/json')


def show_matrix(message):
    print("Loading Matrix LED")
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, width=32, height=8, block_orientation=-90, cascaded=4)
    device.contrast(5)
    device.clear()
    virtual = viewport(device, width=32, height=8)
    show_message(device, f'{message}', fill="white", font=proportional(LCD_FONT), scroll_delay=0.04)


def index(request):
    # Loading index.html
    return render(request, 'index.html')


def homepage(request):
    try:
        print("User authenticated, going to home")
        username = request.session['username']
        id = request.session['id']
        return render(request, 'home.html', {
            'username': username,
            'id': id
        })
    except ValueError as e:
        print('Authenticator failed, going back to index.')
        print(e)
        return render(request, 'index.html')


def logout(request):
    print("Logging user out")
    return redirect('/')
