import time
import json
import asyncio

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages

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
from steam import steam_api, search_sort_utils, utils, rp_utils

GPIO.setwarnings(False)
isLoaded = False
servo = 4
GPIO.setup(servo, GPIO.OUT)
servopos = 0

class ProcessThread(Thread):
    def __init__(self, percentage):
        Thread.__init__(self)
        self.percentage = percentage

    def run(self):
        self.set_servo(self.percentage)

        # set_servo(0)
        time.sleep(1.5)
        # set_servo(25)
        # time.sleep(1.5)
        # set_servo(50)
        # time.sleep(1.5)
        # set_servo(75)
        # time.sleep(1.5)
        # set_servo(100)
        # time.sleep(1.5)
        # self.set_servo(0)
        # time.sleep(1.5)


    def pulse(self, pin_nr, high_time, low_time):
        GPIO.setup(pin_nr, GPIO.OUT)
        GPIO.output(pin_nr, GPIO.HIGH)
        time.sleep(high_time)
        GPIO.output(pin_nr, GPIO.LOW)
        time.sleep(low_time)

    def servo_pulse(self, pin_nr, position):
        self.pulse(pin_nr, (((2 / 100) * position) + 0.5) / 1000, 0.02)

    def set_servo(self, pos):
        global servopos

        while True:
            if servopos > pos:
                servopos -= 1
            elif servopos < pos:
                servopos += 1
            else:
                break
            self.servo_pulse(servo, 100 - servopos)
#
# class ProcessThread(Thread):
#     def __init__(self, name):
#         Thread.__init__(self)
#         self.name = name
#         self.started = datetime.now()
#
#     def run(self):
#         print("Show matrix on different thread")
#         show_matrix(f'Hello {self.name}')

# class ProcessThread(Thread):
#     def __init__(self):
#             Thread.__init__(self)
#
#     def run(self):
#             print("Run schuifregister on different thread")
#             GPIO.setwarnings(False)
#             GPIO.setmode(GPIO.BCM)
#             GPIO.setup(13, GPIO.OUT)
#             GPIO.setup(5, GPIO.OUT)
#             GPIO.setup(6, GPIO.OUT)
#
#             global stop_thread
#
#             while not stop_thread:
#                     for y in range(8):
#                         GPIO.output(13, 1)
#                         controlLeds()
#
#                     for y in range(8):
#                         GPIO.output(13, 0)
#                         controlLeds()
#             print('status changes, killling thread')

# class ProcessThread(Thread):
#     def __init__(self):
#             Thread.__init__(self)
#
#     def run(self):
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setwarnings(0)
#
#         switch = 23
#
#         GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#
#         # Twee knoppen
#         while True:
#             if GPIO.input(switch):
#                 print('Button Pressed!')
#             time.sleep(0.1)
#             print('status changes, killling thread')

# class ProcessThread(Thread):
#     def __init__(self):
#             Thread.__init__(self)
#
#     def run(self):
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setwarnings(0)
#
#         clock_pin = 19
#         data_pin = 26
#
#         GPIO.setup(clock_pin, GPIO.OUT)
#         GPIO.setup(data_pin, GPIO.OUT)
#
#         progress = 0
#
#         blue = [8, 0, 0]
#         green = [0, 255, 0]
#         red = [0, 0, 255]
#         white = [0, 0, 0]
#         delay = 1
#         n = 8
#         global isLoaded
#         print(f'Fetching data progress: {progress}%')
#
#         while not isLoaded:
#             for x in range(0, n):
#                 progress += 12.5
#                 print(f'Fetching data progress: {progress}%')
#                 self.apa102(clock_pin, data_pin, self.colors(x, n, green, white))
#                 time.sleep(delay)
#
#         GPIO.cleanup()
#         print('status changed, killling thread')
#
#     def apa102_send_bytes(self, clock_pin, data_pin, bytes):
#         """
#         zend de bytes naar de APA102 LED strip die is aangesloten op de clock_pin en data_pin
#         """
#
#         # implementeer deze functie:
#
#         # zend iedere byte in bytes:
#         #    zend ieder bit in byte:
#         #       maak de data pin hoog als het bit 1 is, laag als het 0 is
#         #       maak de clock pin hoog
#         #       maak de clock pin laag
#
#         for byte in bytes:
#             for bit in byte:
#                 GPIO.output(data_pin, GPIO.HIGH if bit == '1' else GPIO.LOW)
#                 GPIO.output(clock_pin, GPIO.HIGH)
#                 GPIO.output(clock_pin, GPIO.LOW)
#
#     def apa102(self, clock_pin, data_pin, colors):
#         """
#         zend de colors naar de APA102 LED strip die is aangesloten op de clock_pin en data_pin
#
#         De colors moet een list zijn, met ieder list element een list van 3 integers,
#         in de volgorde [ blauw, groen, rood ].
#         Iedere kleur moet in de range 0..255 zijn, 0 voor uit, 255 voor vol aan.
#
#         bv: colors = [ [ 0, 0, 0 ], [ 255, 255, 255 ], [ 128, 0, 0 ] ]
#         zet de eerste LED uit, de tweede vol aan (wit) en de derde op blauw, halve strekte.
#         """
#
#         # implementeer deze functie, maak gebruik van de apa102_send_bytes functie
#
#         # zend eerst 4 bytes met nullen
#         # zend dan voor iedere pixel:
#         #    eerste een byte met allemaal enen
#         #    dan de 3 bytes met de kleurwaarden
#         # zend nog 4 bytes, maar nu met allemaal enen
#         self.apa102_send_bytes(clock_pin, data_pin, [f'{0:08b}' for e in range(0, 4)])
#         for pixel in colors:
#             array = [f'{255:08b}', f'{pixel[0]:08b}', f'{pixel[1]:08b}', f'{pixel[2]:08b}']
#             self.apa102_send_bytes(clock_pin, data_pin, array)
#         self.apa102_send_bytes(clock_pin, data_pin, [f'{255:08b}' for e in range(0, 4)])
#
#     def colors(self, x, n, on, off):
#         result = []
#         for i in range(0, n):
#             if i <= x:
#                 result.append(on)
#             else:
#                 result.append(off)
#         return result


# def ajax_view(request):
#     print('Running RFID')
#     reader = SimpleMFRC522()
#     try:
#         id, text = reader.read()
#         username = text
#         card_id = id
#         print(f'User: {username}\nId: {id}')
#         request.session['username'] = username
#         request.session['id'] = card_id
#         my_thread = ProcessThread(username)
#         my_thread.start()
#     # except Exception as e:
#     #     print(f'Caught exception!: {e}')
#     finally:
#         GPIO.cleanup()
#
#     context = {
#         "gebruikersnaam": username,
#         "card_id": card_id
#     }
#
#     data = json.dumps(context)
#
#     return HttpResponse(data, content_type='application/json')


# def show_matrix(message):
#     print("Loading Matrix LED")
#     serial = spi(port=0, device=0, gpio=noop())
#     device = max7219(serial, width=32, height=8, block_orientation=-90, cascaded=4)
#     device.contrast(5)
#     device.clear()
#     virtual = viewport(device, width=32, height=8)
#     show_message(device, f'{message}', fill="white", font=proportional(LCD_FONT), scroll_delay=0.01)


def homepage(request):
    # Loading index.html
    return render(request, 'index.html')


# def homepage(request):
#     try:
#         print("User authenticated, going to home")
#         username = request.session['username']
#         id = request.session['id']
#         return render(request, 'home.html', {
#             'username': username,
#             'id': id
#         })
#     except ValueError as e:
#         print('Authenticator failed, going back to index.')
#         print(e)
#         return render(request, 'index.html')


def logout(request):
    print("Logging user out")
    return redirect('/')

def fetch_steam_data_ajax(request, reverse=False):
    print('Starting process')
    my_thread = ProcessThread(0)
    my_thread.start()
    apps = steam_api.fetch_all_apps()
    sorted_apps = search_sort_utils.merge_recursive(apps, key='appid')
    context = {
        'apps': sorted_apps,
        'reverse': reverse
    }

    global isLoaded
    isLoaded = True
    # my_thread.join()

    data = json.dumps(context)

    return HttpResponse(data, content_type='application/json')

def fetch_details_ajax(request, appid):
    details = steam_api.fetch_details(appid)
    details_ss = steam_api.fetch_details_steamspy(appid)
    success = utils.isValidDetails(details, appid)
    if not success:
        messages.info(request, f'Game id {appid} does not have any details :(')

    try:
        likes = details_ss['positive']
        dislikes = details_ss['negative']
        total = likes + dislikes
        if likes == 0 or dislikes == 0:
            if likes == 0:
                percentage = 0
            else:
                percentage = 100
        else:
            percentage = int(100 - (total / dislikes))

        my_thread = ProcessThread(percentage)
        my_thread.start()
    except ZeroDivisionError:
        print(f"Likes: {details_ss['positive']}, dislikes: {details_ss['negative']}")

    context = {
        'details': details,
        'details_ss': details_ss,
        'success': success
    }

    data = json.dumps(context)
    return HttpResponse(data, content_type='application/json')


def start_servo(request, percentage):
    print('Called')
    GPIO.setmode(GPIO.BCM)

    def pulse(pin_nr, high_time, low_time):
        GPIO.setup(pin_nr, GPIO.OUT)
        GPIO.output(pin_nr, GPIO.HIGH)
        time.sleep(high_time)
        GPIO.output(pin_nr, GPIO.LOW)
        time.sleep(low_time)

    def servo_pulse(pin_nr, position):
        pulse(pin_nr, (((2 / 100) * position) + 0.5) / 1000, 0.02)

    servo = 4
    GPIO.setup(servo, GPIO.OUT)
    servopos = 0

    def set_servo(pos):
        global servopos

        while True:
            if servopos > pos:
                servopos -= 1
            elif servopos < pos:
                servopos += 1
            else:
                break
            servo_pulse(servo, 100 - servopos)

    # Testing intervals of 25%
    givenpos = int(percentage)
    set_servo(givenpos)

    # set_servo(0)
    time.sleep(1.5)
    # set_servo(25)
    # time.sleep(1.5)
    # set_servo(50)
    # time.sleep(1.5)
    # set_servo(75)
    # time.sleep(1.5)
    # set_servo(100)
    # time.sleep(1.5)
    set_servo(0)
    time.sleep(1.5)

    return HttpResponse('1')

def app_details(request, appid):
    return render(request, 'details.html', {
        'appid': appid
    })

def controlLeds():
    time.sleep(0.1)
    GPIO.output(5, 1)
    time.sleep(0.1)
    GPIO.output(5, 0)
    GPIO.output(13, 0)
    GPIO.output(6, 1)
    time.sleep(0.1)
    GPIO.output(6, 0)
