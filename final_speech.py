#!/usr/bin/env python3

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.screenmanager import Screen
from control import Arduino
from wakeonlan import wol
from mysql.connector import Error
from wmi_client_wrapper import wrapper
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from kivy.properties import ObjectProperty

from apscheduler.schedulers.background import BackgroundScheduler

# REMOVE THIS EXCEPTION IF NOT DEBUGGING
from control import SerialException

import socket
import time
import os
import random
import mysql.connector
import json
import smtplib
import speech_recognition as sr
from threading import Thread
###################################################################################################################
try:
    control=Arduino()
except SerialException:
    from unittest.mock import Mock

    control=Mock()

try:
    propertiesFile=os.path.dirname(
        os.path.realpath('__file__')) + "/properties.json"
    fprop=open(propertiesFile)
    loadprop=json.load(fprop)

    PC_MAC_ADDRESS=loadprop["pc_mac_address"]
    PC_HOSTNAME=loadprop["pc_hostname"]
    HOSTNAME=loadprop["hostname"]
    NEEDS_WOL_PROXY=loadprop["needs_wol_proxy"]
    WOL_PROXY_SERVER=loadprop["wol_proxy_server"]

    DVD_VCR_PLAY=loadprop["dvd_vcr_play"]
    DVD_VCR_STOP=loadprop["dvd_vcr_stop"]
    DVD_VCR_PAUSE=loadprop["dvd_vcr_pause"]
    DVD_VCR_REW=loadprop["dvd_vcr_rew"]
    DVD_VCR_FF=loadprop["dvd_vcr_ff"]
    DVD_VCR_EJECT=loadprop["dvd_vcr_eject"]
    DVD_VCR_CHAN0=loadprop["dvd_vcr_chan0"]
    DVD_VCR_CHAN_BLANK=loadprop["dvd_vcr_chan_blank"]
    DVD_VCR_CHAN3=loadprop["dvd_vcr_chan3"]
    DVD_VCR_CHANDOWN=loadprop["dvd_vcr_chandown"]
    DVD_VCR_VCR=loadprop["dvd_vcr_vcr"]
    DVD_VCR_DVD=loadprop["dvd_vcr_dvd"]

    DVD_VCR_PLAY_TYPE=loadprop["dvd_vcr_play_type"]
    DVD_VCR_STOP_TYPE=loadprop["dvd_vcr_stop_type"]
    DVD_VCR_PAUSE_TYPE=loadprop["dvd_vcr_pause_type"]
    DVD_VCR_REW_TYPE=loadprop["dvd_vcr_rew_type"]
    DVD_VCR_FF_TYPE=loadprop["dvd_vcr_ff_type"]
    DVD_VCR_EJECT_TYPE=loadprop["dvd_vcr_eject_type"]
    DVD_VCR_CHAN0_TYPE=loadprop["dvd_vcr_chan0_type"]
    DVD_VCR_CHAN_BLANK_TYPE=loadprop["dvd_vcr_chan_blank_type"]
    DVD_VCR_CHAN3_TYPE=loadprop["dvd_vcr_chan3_type"]
    DVD_VCR_CHANDOWN_TYPE=loadprop["dvd_vcr_chandown_type"]
    DVD_VCR_VCR_TYPE=loadprop["dvd_vcr_vcr_type"]
    DVD_VCR_DVD_TYPE=loadprop["dvd_vcr_dvd_type"]

    DOC_CAM_OFF=loadprop["doc_cam_off"]
    DOC_CAM_ON=loadprop["doc_cam_on"]
    DOC_CAM_SOURCE_PRESENTER=loadprop["doc_cam_source_presenter"]
    DOC_CAM_SERIAL_CONFIG=loadprop["doc_cam_serial_config"]

    CABLE_CHAN_UP=loadprop["cable_chan_up"]
    CABLE_CHAN_DOWN=loadprop["cable_chan_down"]
    CABLE_CHAN_ZERO=loadprop["cable_chan_zero"]
    CABLE_CHAN_ONE=loadprop["cable_chan_one"]
    CABLE_CHAN_TWO=loadprop["cable_chan_two"]
    CABLE_CHAN_THREE=loadprop["cable_chan_three"]
    CABLE_CHAN_FOUR=loadprop["cable_chan_four"]
    CABLE_CHAN_FIVE=loadprop["cable_chan_five"]
    CABLE_CHAN_SIX=loadprop["cable_chan_six"]
    CABLE_CHAN_SEVEN=loadprop["cable_chan_seven"]
    CABLE_CHAN_EIGHT=loadprop["cable_chan_eight"]
    CABLE_CHAN_NINE=loadprop["cable_chan_nine"]

    CABLE_CHAN_UP_TYPE=loadprop["cable_chan_up_type"]
    CABLE_CHAN_DOWN_TYPE=loadprop["cable_chan_down_type"]
    CABLE_CHAN_ZERO_TYPE=loadprop["cable_chan_zero_type"]
    CABLE_CHAN_ONE_TYPE=loadprop["cable_chan_one_type"]
    CABLE_CHAN_TWO_TYPE=loadprop["cable_chan_two_type"]
    CABLE_CHAN_THREE_TYPE=loadprop["cable_chan_three_type"]
    CABLE_CHAN_FOUR_TYPE=loadprop["cable_chan_four_type"]
    CABLE_CHAN_FIVE_TYPE=loadprop["cable_chan_five_type"]
    CABLE_CHAN_SIX_TYPE=loadprop["cable_chan_six_type"]
    CABLE_CHAN_SEVEN_TYPE=loadprop["cable_chan_seven_type"]
    CABLE_CHAN_EIGHT_TYPE=loadprop["cable_chan_eight_type"]
    CABLE_CHAN_NINE_TYPE=loadprop["cable_chan_nine_type"]

    PROJECTOR_WIFI_COLLAB=loadprop["projector_wifi_collab"]
    PROJECTOR_ON=loadprop["projector_on"]
    PROJECTOR_OFF=loadprop["projector_off"]
    PROJECTOR_LAPTOP_SOURCE_VGA=loadprop["projector_laptop_source_vga"]
    PROJECTOR_LAPTOP_SOURCE_HDMI=loadprop["projector_laptop_source_hdmi"]
    PROJECTOR_USB=loadprop["projector_usb"]
    PROJECTOR_HDMI1=loadprop["projector_hdmi1"]
    PROJECTOR_DVD=loadprop["projector_dvd"]
    PROJECTOR_VGA2=loadprop["projector_vga2"]
    PROJECTOR_MUTE_ON=loadprop["projector_mute_on"]
    PROJECTOR_MUTE_OFF=loadprop["projector_mute_off"]
    PROJECTOR_SERIAL_CONFIG=loadprop["projector_serial_config"]

    AUDIO_MIN_VOLUME_DB=loadprop["audio_min_volume_db"]
    AUDIO_MAX_VOLUME_DB=loadprop["audio_max_volume_db"]
    STARTUP_VOLUME_LEVEL=loadprop["audio_device_startup_volume"]

    ARDUINO_IS_MIXER=loadprop["arduino_is_mixer"]

    EMAIL_HELPDESK_RECIPIENTS=loadprop["email_helpdesk_recipients"]

    DATABASE_HOST=loadprop["database_host"]
    DATABASE_NAME=loadprop["database_name"]
    DATABASE_USER=loadprop["database_user"]
    DATABASE_PASSWORD=loadprop["database_password"]

    DOMAIN_ADMIN_USERNAME=loadprop["domain_admin_username"]
    DOMAIN_ADMIN_PASSWORD=loadprop["domain_admin_password"]

    IS_DOC_CAM_AVAILABLE=loadprop["is_doc_cam_available"]
    IS_CABLE_AVAILABLE=loadprop["is_cable_available"]

    DEFAULT_STARTUP_VGA_SRC=loadprop["default_startup_vga_src"]

    DEFAULT_PC_AUDIO_TYPE=loadprop["default_pc_audio_type"]
    IS_LAPTOP_HDMIT_AVAILABLE=loadprop["is_laptop_hdmi_available"]

    fprop.close()

except (FileNotFoundError, KeyError) as e:
    print(e)

    PC_MAC_ADDRESS='00-00-00-00-00-00'
    PC_HOSTNAME='Unknown'
    HOSTNAME='Unknown'
    NEEDS_WOL_PROXY='no'
    WOL_PROXY_SERVER='0.0.0.0'

    DVD_VCR_PLAY='0x0000000'
    DVD_VCR_STOP='0x0000000'
    DVD_VCR_PAUSE='0x0000000'
    DVD_VCR_REW='0x0000000'
    DVD_VCR_FF='0x0000000'
    DVD_VCR_EJECT='0x0000000'
    DVD_VCR_CHAN0='0x0000000'
    DVD_VCR_CHAN_BLANK='0x0000000'
    DVD_VCR_CHAN3='0x0000000'
    DVD_VCR_CHANDOWN='0x0000000'
    DVD_VCR_VCR='0x0000000'
    DVD_VCR_DVD='0x0000000'

    DVD_VCR_PLAY_TYPE='p'
    DVD_VCR_STOP_TYPE='p'
    DVD_VCR_PAUSE_TYPE='p'
    DVD_VCR_REW_TYPE='p'
    DVD_VCR_FF_TYPE='p'
    DVD_VCR_EJECT_TYPE='p'
    DVD_VCR_CHAN0_TYPE='p'
    DVD_VCR_CHAN_BLANK_TYPE='p'
    DVD_VCR_CHAN3_TYPE='p'
    DVD_VCR_CHANDOWN_TYPE='p'
    DVD_VCR_VCR_TYPE='p'
    DVD_VCR_DVD_TYPE='p'

    DOC_CAM_OFF='B\\x01\\x21'
    DOC_CAM_ON='BAa'
    DOC_CAM_SOURCE_PRESENTER='BLI'
    DOC_CAM_SERIAL_CONFIG='9600n81'

    CABLE_CHAN_UP='0,0,0,0,'
    CABLE_CHAN_DOWN='0,0,0,0,'
    CABLE_CHAN_ZERO='0,0,0,0,'
    CABLE_CHAN_ONE='0,0,0,0,'
    CABLE_CHAN_TWO='0,0,0,0,'
    CABLE_CHAN_THREE='0,0,0,0,'
    CABLE_CHAN_FOUR='0,0,0,0,'
    CABLE_CHAN_FIVE='0,0,0,0,'
    CABLE_CHAN_SIX='0,0,0,0,'
    CABLE_CHAN_SEVEN='0,0,0,0,'
    CABLE_CHAN_EIGHT='0,0,0,0,'
    CABLE_CHAN_NINE='0,0,0,0,'

    CABLE_CHAN_UP_TYPE='r'
    CABLE_CHAN_DOWN_TYPE='r'
    CABLE_CHAN_ZERO_TYPE='r'
    CABLE_CHAN_ONE_TYPE='r'
    CABLE_CHAN_TWO_TYPE='r'
    CABLE_CHAN_THREE_TYPE='r'
    CABLE_CHAN_FOUR_TYPE='r'
    CABLE_CHAN_FIVE_TYPE='r'
    CABLE_CHAN_SIX_TYPE='r'
    CABLE_CHAN_SEVEN_TYPE='r'
    CABLE_CHAN_EIGHT_TYPE='r'
    CABLE_CHAN_NINE_TYPE='r'

    PROJECTOR_WIFI_COLLAB=''
    PROJECTOR_ON=''
    PROJECTOR_OFF=''
    PROJECTOR_LAPTOP_SOURCE_VGA=''
    PROJECTOR_LAPTOP_SOURCE_HDMI=''
    PROJECTOR_USB=''
    PROJECTOR_HDMI1=''
    PROJECTOR_DVD=''
    PROJECTOR_VGA2=''
    PROJECTOR_MUTE_ON=''
    PROJECTOR_MUTE_OFF=''
    PROJECTOR_SERIAL_CONFIG='9600n81'

    AUDIO_MIN_VOLUME_DB=0
    AUDIO_MAX_VOLUME_DB=128
    STARTUP_VOLUME_LEVEL=30

    ARDUINO_IS_MIXER='false'

    EMAIL_HELPDESK_RECIPIENTS='tllos1@uis.edu'

    DATABASE_HOST='localhost'
    DATABASE_NAME='uisipi'
    DATABASE_USER='uisipi'
    DATABASE_PASSWORD=''

    DOMAIN_ADMIN_USERNAME='Administrator'
    DOMAIN_ADMIN_PASSWORD=''

    IS_DOC_CAM_AVAILABLE='false'
    IS_CABLE_AVAILABLE='false'

    DEFAULT_STARTUP_VGA_SRC='hdmi'

    DEFAULT_PC_AUDIO_TYPE='composite'
    IS_LAPTOP_HDMIT_AVAILABLE='false'


###################################################################################################################


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        # analyze the audio source for 1 second
        recognizer.adjust_for_ambient_noise(source)
        audio=recognizer.listen(source)

    # set up the response object
    response={
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #   update the response object accordingly
    try:
        response["transcription"]=recognizer.recognize_sphinx(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"]=False
        response["error"]="API unavailable/unresponsive"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"]="Unable to recognize speech"

    return response


def initialize_global_vars():
    global IP_ADDRESS, USERNAME, VOICE_COM, SESSIONID, CURRENT_LAPTOP_SRC
    IP_ADDRESS='0.0.0.0'
    USERNAME='Unknown'
    VOICE_COM='Unknown'
    SESSIONID=0
    CURRENT_LAPTOP_SRC=DEFAULT_STARTUP_VGA_SRC


def capture_speech_from_mic():
    global VOICE_COM
    r=sr.Recognizer()
    m=sr.Microphone()
    words=""
    try:
        words=recognize_speech_from_mic(r, m)
    except Exception as e:
        print("Exception" + str(e))
    if words is not None:
        return words

def main_test():
    m=MainScreen()
    m.system_on()



def get_username():
    global USERNAME
    try:
        wmic=wrapper.WmiClientWrapper(
            username=DOMAIN_ADMIN_USERNAME, password=DOMAIN_ADMIN_PASSWORD, host=PC_HOSTNAME)
        USERNAME=str(wmic.query("SELECT Username FROM win32_computersystem"))

    except Exception as exception:
        USERNAME='Unknown username for ' + PC_HOSTNAME


def set_random_variable():
    global SESSIONID
    random.seed(time.time())
    SESSIONID=random.randint(100000000, 900000000)
    SESSIONID+=1


def get_ip():
    global IP_ADDRESS
    sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    with sock:
        try:
            sock.connect(('1.1.1.1', 0))
            ip=socket.gethostname() + " (" + sock.getsockname()[0] + ")"
        except OSError:
            ip=HOSTNAME
        finally:
            IP_ADDRESS=ip


def get_timedate():
    return time.strftime('%a, %b %d, %Y %I:%M %p', time.localtime())


def wakeup_pc():
    try:
        if NEEDS_WOL_PROXY == 'no':
            wol.send_magic_packet(PC_MAC_ADDRESS)
        else:
            wol.send_magic_packet(
                PC_MAC_ADDRESS, ip_address=WOL_PROXY_SERVER, port=9)
    except OSError:
        if NEEDS_WOL_PROXY == 'no':
            Clock.schedule_once(
                lambda dt: wol.send_magic_packet(PC_MAC_ADDRESS), 15)
        else:
            Clock.schedule_once(lambda dt: wol.send_magic_packet(
                PC_MAC_ADDRESS, ip_address=WOL_PROXY_SERVER, port=9), 15)

    except ValueError as e:
        print(e)


def insertButtonPress(sessionid, username, roomname, button_pressed):
    query=("INSERT INTO uisipi_usage (sessionid, username, roomname, button_pressed) VALUES(%s, %s, %s, %s)")
    args=(sessionid, username, roomname, button_pressed)

    try:
        conn=mysql.connector.connect(
            host=DATABASE_HOST, database=DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD)
        cursor=conn.cursor()

        cursor.execute(query, args)
        conn.commit()

    except Error as e:
        print(e)

    else:
        cursor.close()
        conn.close()


def isRoomOn(roomname):
    isOn=False

    query=(
        "select button_pressed from uisipi_usage where roomname LIKE %s and button_pressed IN ('ON', 'OFF', 'REBOOT-SCHEDULED') order by date_of_press DESC LIMIT 1")
    args=(roomname)

    try:
        conn=mysql.connector.connect(
            host=DATABASE_HOST, database=DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD)
        cursor=conn.cursor()
        cursor.execute(query, (args,))

        row=cursor.fetchone()

        if row is not None:
            if row[0] == 'ON':
                isOn=True

    except Error as e:
        print(e)

    else:
        cursor.close()
        conn.close()

    return isOn


def projector_config():
    control._write(rb's', rb'2', rb'c', PROJECTOR_SERIAL_CONFIG.encode('utf-8'))

def doc_cam_config():
    control._write(rb's', rb'3', rb'c', DOC_CAM_SERIAL_CONFIG.encode('utf-8'))


# DISABLE E


def audio_mixer_select_mute():
    control.serial.write(b'\x02d4h\x03')


# ENABLE E


def audio_mixer_select_unmute():
    control.serial.write(b'\x02d4l\x03')


# INPUT 0 = 000


def audio_mixer_select_input_zero():
    control.serial.write(b'\x02d1l\x03')
    control.serial.write(b'\x02d2l\x03')
    control.serial.write(b'\x02d3l\x03')


# INPUT 4 = 001


def audio_mixer_select_pc():
    control.serial.write(b'\x02d1l\x03')
    control.serial.write(b'\x02d2l\x03')
    control.serial.write(b'\x02d3h\x03')


# INPUT 5 = 101


def audio_mixer_select_laptop():
    control.serial.write(b'\x02d1h\x03')
    control.serial.write(b'\x02d2l\x03')
    control.serial.write(b'\x02d3h\x03')


# INPUT 2 = 010


def audio_mixer_select_dvd():
    control.serial.write(b'\x02d1l\x03')
    control.serial.write(b'\x02d2h\x03')
    control.serial.write(b'\x02d3l\x03')


# INPUT 3 = 110


def audio_mixer_select_projector():
    control.serial.write(b'\x02d1h\x03')
    control.serial.write(b'\x02d2h\x03')
    control.serial.write(b'\x02d3l\x03')


def digital_config():
    # Configure Arduino digital ports 30-33 as digital outputs then disable all sound
    control.serial.write(b'\x02d1o\x03')
    control.serial.write(b'\x02d2o\x03')
    control.serial.write(b'\x02d3o\x03')
    control.serial.write(b'\x02d4o\x03')

    audio_mixer_select_input_zero()
    audio_mixer_select_mute()


def projector_wifi_collab():
    control._write(rb's', rb'2', rb's', PROJECTOR_WIFI_COLLAB.encode('utf-8'))


def projector_on():
    control._write(rb's', rb'2', rb's', PROJECTOR_ON.encode('utf-8'))


def projector_off():
    control._write(rb's', rb'2', rb's', PROJECTOR_OFF.encode('utf-8'))


def projector_laptop_vga():
    control._write(rb's', rb'2', rb's',
                   PROJECTOR_LAPTOP_SOURCE_VGA.encode('utf-8'))


def projector_laptop_hdmi():
    control._write(rb's', rb'2', rb's',
                   PROJECTOR_LAPTOP_SOURCE_HDMI.encode('utf-8'))


def projector_usb():
    control._write(rb's', rb'2', rb's', PROJECTOR_USB.encode('utf-8'))


def projector_hdmi1():
    control._write(rb's', rb'2', rb's', PROJECTOR_HDMI1.encode('utf-8'))


def projector_dvd():
    control._write(rb's', rb'2', rb's', PROJECTOR_DVD.encode('utf-8'))


def dvd_source_dvd():
    # DVD button
    control._write(rb'i', rb'9', DVD_VCR_DVD_TYPE.encode(
        'utf-8'), DVD_VCR_DVD.encode('utf-8'))


def dvd_source_vcr():
    # VCR LINE 1
    # VCR button
    control._write(rb'i', rb'9', DVD_VCR_VCR_TYPE.encode(
        'utf-8'), DVD_VCR_VCR.encode('utf-8'))
    # CHAN 0
    control._write(rb'i', rb'9', DVD_VCR_CHAN0_TYPE.encode(
        'utf-8'), DVD_VCR_CHAN0.encode('utf-8'))
    # CHAN blank - 2 o 4
    control._write(rb'i', rb'9', DVD_VCR_CHAN_BLANK_TYPE.encode(
        'utf-8'), DVD_VCR_CHAN_BLANK.encode('utf-8'))
    # CHAN DOWN
    control._write(rb'i', rb'9', DVD_VCR_CHANDOWN_TYPE.encode(
        'utf-8'), DVD_VCR_CHANDOWN.encode('utf-8'))


def projector_cable():
    control._write(rb's', rb'2', rb's', PROJECTOR_DVD.encode('utf-8'))
    # VCR button
    control._write(rb'i', rb'9', DVD_VCR_VCR_TYPE.encode(
        'utf-8'), DVD_VCR_VCR.encode('utf-8'))
    # 0
    control._write(rb'i', rb'9', DVD_VCR_CHAN0_TYPE.encode(
        'utf-8'), DVD_VCR_CHAN0.encode('utf-8'))
    # 3
    control._write(rb'i', rb'9', DVD_VCR_CHAN3_TYPE.encode(
        'utf-8'), DVD_VCR_CHAN3.encode('utf-8'))


def doc_cam_on():
    control._write(rb's', rb'2', rb's', PROJECTOR_VGA2.encode('utf-8'))
    control._write(rb's', rb'3', rb's', DOC_CAM_ON.encode('utf-8'))
    control._write(rb's', rb'3', rb's',
                   DOC_CAM_SOURCE_PRESENTER.encode('utf-8'))


def doc_cam_off():
    control._write(rb's', rb'3', rb's', DOC_CAM_OFF.encode('utf-8'))


def cable_chan_up():
    control._write(rb'i', rb'9', CABLE_CHAN_UP_TYPE.encode(
        'utf-8'), CABLE_CHAN_UP.encode('utf-8'))


def cable_chan_down():
    control._write(rb'i', rb'9', CABLE_CHAN_DOWN_TYPE.encode(
        'utf-8'), CABLE_CHAN_DOWN.encode('utf-8'))


def cable_chan_zero():
    control._write(rb'i', rb'9', CABLE_CHAN_ZERO_TYPE.encode(
        'utf-8'), CABLE_CHAN_ZERO.encode('utf-8'))


def cable_chan_one():
    control._write(rb'i', rb'9', CABLE_CHAN_ONE_TYPE.encode(
        'utf-8'), CABLE_CHAN_ONE.encode('utf-8'))


def cable_chan_two():
    control._write(rb'i', rb'9', CABLE_CHAN_TWO_TYPE.encode(
        'utf-8'), CABLE_CHAN_TWO.encode('utf-8'))


def cable_chan_three():
    control._write(rb'i', rb'9', CABLE_CHAN_THREE_TYPE.encode(
        'utf-8'), CABLE_CHAN_THREE.encode('utf-8'))


def cable_chan_four():
    control._write(rb'i', rb'9', CABLE_CHAN_FOUR_TYPE.encode(
        'utf-8'), CABLE_CHAN_FOUR.encode('utf-8'))


def cable_chan_five():
    control._write(rb'i', rb'9', CABLE_CHAN_FIVE_TYPE.encode(
        'utf-8'), CABLE_CHAN_FIVE.encode('utf-8'))


def cable_chan_six():
    control._write(rb'i', rb'9', CABLE_CHAN_SIX_TYPE.encode(
        'utf-8'), CABLE_CHAN_SIX.encode('utf-8'))


def cable_chan_seven():
    control._write(rb'i', rb'9', CABLE_CHAN_SEVEN_TYPE.encode(
        'utf-8'), CABLE_CHAN_SEVEN.encode('utf-8'))


def cable_chan_eight():
    control._write(rb'i', rb'9', CABLE_CHAN_EIGHT_TYPE.encode(
        'utf-8'), CABLE_CHAN_EIGHT.encode('utf-8'))


def cable_chan_nine():
    control._write(rb'i', rb'9', CABLE_CHAN_NINE_TYPE.encode(
        'utf-8'), CABLE_CHAN_NINE.encode('utf-8'))


def reset_devices():
    if ARDUINO_IS_MIXER == 'true':
        audio_mixer_select_input_zero()
        audio_mixer_select_mute()

    projector_off()
    doc_cam_off()
    dvd_source_vcr()


###################################################################################################################
initialize_global_vars()
# capture_speech_from_mic()
OFF_WHITE=(.9, .9, .9, 1)


###################################################################################################################


class MainScreen(Screen):
    dvd_p=ObjectProperty(None)
    cable_p=ObjectProperty(None)
    pc_p=ObjectProperty(None)
    doccam_p=ObjectProperty(None)
    wificollab_p=ObjectProperty(None)
    laptop_p=ObjectProperty(None)
    shared_screen_p=ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.button_set=False

    def scheduled_reboot(self):
        if isRoomOn(HOSTNAME + '%'):
            reset_devices()
            insertButtonPress(SESSIONID, USERNAME,
                              HOSTNAME, 'REBOOT-SCHEDULED')
            Clock.schedule_once(lambda dt: os.system('reboot now'), 10)

    def on_enter(self):
        def initialize_buttons(dt):
            self.ids.off.state='down'
            Clock.schedule_once(lambda dt: self.disable_buttons(), 1)
            Clock.schedule_interval(lambda dt: self.update_clock(), 1)

            self.ids.off.disabled=True

        if not self.button_set:
            Clock.schedule_once(initialize_buttons)
            self.button_set=True

            scheduler=BackgroundScheduler()
            scheduler.add_job(self.scheduled_reboot, 'cron',
                              day_of_week='mon-sun', hour=2, minute=0, misfire_grace_time=1000)
            scheduler.start()

    Window.clearcolor=OFF_WHITE

    for group in ('source', 'power'):
        for widget in ToggleButton.get_widgets(group):
            widget.allow_no_selection=False

    def update_clock(self):
        self.ids.header_date.text=get_timedate()

    def disable_buttons(self):
        self.ids.dvd.disabled=True
        self.ids.cable.disabled=True
        self.ids.pc.disabled=True
        self.ids.doccam.disabled=True
        self.ids.wificollab.disabled=True
        self.ids.laptop.disabled=True
        self.parent.parent.ids.shared_screen.vol_slider_p.disabled=True
        self.parent.parent.ids.shared_screen.audio_mute_p.disabled=True
        self.parent.parent.ids.shared_screen.video_mute_p.disabled=True

    def enable_buttons(self):
        if IS_CABLE_AVAILABLE == 'true':
            self.ids.cable.disabled=False

        if IS_DOC_CAM_AVAILABLE == 'true':
            self.ids.doccam.disabled=False

        self.ids.dvd.disabled=False
        self.ids.pc.disabled=False
        self.ids.wificollab.disabled=False
        self.ids.laptop.disabled=False
        self.parent.parent.ids.shared_screen.vol_slider_p.disabled=False
        self.parent.parent.ids.shared_screen.audio_mute_p.disabled=False
        self.parent.parent.ids.shared_screen.video_mute_p.disabled=False

    def disable_off(self):
        self.ids.off.disabled=True

    def disable_on(self):
        self.ids.on.disabled=True

    def blink(self, element, duration, rate):
        def set_style(dt):
            if element.state == 'normal':
                element.state='down'
            elif element.state == 'down':
                element.state='normal'

        def clean_up(dt):
            Clock.unschedule(set_style)

            element.state='down'

            self.ids.on.disabled=False
            self.ids.off.disabled=False

        self.ids.on.disabled=True
        self.ids.off.disabled=True

        Clock.schedule_interval(set_style, rate)
        Clock.schedule_once(clean_up, duration)

    def pc_selected(self, state):
        if state == 'down':
            if ARDUINO_IS_MIXER == 'true':
                if DEFAULT_PC_AUDIO_TYPE == 'composite':
                    audio_mixer_select_pc()
                elif DEFAULT_PC_AUDIO_TYPE == 'hdmi':
                    audio_mixer_select_projector()
                else:
                    audio_mixer_select_pc()

            projector_hdmi1()
            dvd_source_vcr()

            insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'PC')

    def dvd_selected(self, state):
        if state == 'down':
            if ARDUINO_IS_MIXER == 'true':
                audio_mixer_select_dvd()

            projector_dvd()

            insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'DVD-VCR')

    def cable_selected(self, state):
        if state == 'down':
            if ARDUINO_IS_MIXER == 'true':
                audio_mixer_select_dvd()

            projector_cable()

            insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'CABLE-TV')

    def laptop_selected(self, state):
        if state == 'down':

            if CURRENT_LAPTOP_SRC == 'vga':
                projector_laptop_vga()
                if ARDUINO_IS_MIXER == 'true':
                    audio_mixer_select_laptop()
            else:
                projector_laptop_hdmi()
                if ARDUINO_IS_MIXER == 'true':
                    audio_mixer_select_projector()

            dvd_source_vcr()

            insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'LAPTOP')

    def checkifdvdalreadypressed(self, state):
        if state == 'normal':
            self.ids.dvd.state='down'

    def checkifwificollabalreadypressed(self, state):
        if state == 'normal':
            self.ids.wificollab.state='down'

    def checkifdoccamalreadypressed(self, state):
        if state == 'normal':
            self.ids.doccam.state='down'

    def checkiflaptopalreadypressed(self, state):
        if state == 'normal':
            self.ids.laptop.state='down'

    def checkifcablealreadypressed(self, state):
        if state == 'normal':
            self.ids.cable.state='down'

    def wifi_collab_selected(self, state):
        if state == 'down':
            if ARDUINO_IS_MIXER == 'true':
                audio_mixer_select_projector()

            projector_wifi_collab()
            dvd_source_vcr()

            insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'WIFI')

    def doc_cam_selected(self, state):
        if state == 'down':
            if ARDUINO_IS_MIXER == 'true':
                audio_mixer_select_input_zero(
                )
            doc_cam_on()
            dvd_source_vcr()
            insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'DOCCAM')

    def change_screens(self):
        self.parent.parent.ids.screen_management_volume.current='help_tools_screen'
        self.parent.parent.ids.screen_management.current='help_screen'

    # def SpeakCommand(self):
    # 	#This method will get executed when the user press "Speak" button in MainScreen
    # 	global VOICE_COM
    # 	recognizer = sr.Recognizer()
    # 	mic = sr.Microphone(device_index=2)
    # 	try:
    # 		while True:
    # 			response = recognize_speech_from_mic(recognizer, mic)
    # 			if response['success'] == True:
    # 				VOICE_COM = response['transcription'];
    #
    # 				switch VOICE_COM:
    # 					case "system on":
    # 					case "turn on system":self.system_on();
    # 										  break;
    # 					case "system off":
    # 					case "turn off system":self.system_off();
    # 									       break;
    # 					case "volume up":
    # 					case "increase volume":self.volume_up();
    # 										   break;
    # 					case "volume down":
    # 					case "decrease volume":self.volume_down();
    # 										  break;
    # 					default:
    # 							print("I did not understand what you just asked me to do. or Its an Invalid command")
    # 	except KeyboardInterrupt:
    # 		pass

    def system_on(self):
        self.ids.off.state='normal'
        self.parent.parent.ids.shared_screen.vol_slider_p.value=float(
            STARTUP_VOLUME_LEVEL)
        self.blink(self.ids.on, 25, .5)

        Clock.schedule_once(lambda dt: self.ids.pc.trigger_action(), 15)
        projector_on()
        wakeup_pc()
        wakeup_pc()

        set_random_variable()
        Clock.schedule_once(lambda dt: get_username(), 300)
        Clock.schedule_once(lambda dt: get_ip(), 10)

        Clock.schedule_once(lambda dt: insertButtonPress(
            SESSIONID, USERNAME, IP_ADDRESS, 'ON'), 12)

        # call projector_hdmi1 in 15 seconds -  Schedule a function that doesnt accept the dt argument, you can use a lambda expression to write a short function that does accept dt
        Clock.schedule_once(lambda dt: projector_hdmi1(), 15)

        if ARDUINO_IS_MIXER == 'true':
            Clock.schedule_once(lambda dt: audio_mixer_select_unmute(), 17)


        Clock.schedule_once(lambda dt: self.enable_buttons(), 25)
        Clock.schedule_once(lambda dt: self.disable_on(), 28)

    def system_off(self):
        self.blink(self.ids.off, 15, .5)
        reset_devices()
        self.parent.parent.ids.shared_screen.vol_slider_p.value=0

        self.ids.dvd.state='normal'
        self.ids.cable.state='normal'
        self.ids.pc.state='normal'
        self.ids.doccam.state='normal'
        self.ids.wificollab.state='normal'
        self.ids.laptop.state='normal'

        Clock.schedule_once(lambda dt: insertButtonPress(
            SESSIONID, USERNAME, IP_ADDRESS, 'OFF'), 1)
        Clock.schedule_once(lambda dt: initialize_global_vars(), 2)

        Clock.schedule_once(lambda dt: self.disable_buttons(), 1)
        Clock.schedule_once(lambda dt: self.disable_off(), 18)

    def volume_up(self):
        if self.parent.parent.ids.shared_screen.vol_slider_p.value < AUDIO_MAX_VOLUME_DB:
            shared_screen_p.audio_control_volume(self.parent.parent.ids.shared_screen.vol_slider_p + 1)
        else:
            print("Reached Max Volume")

    def volume_down(self):
            if self.parent.parent.ids.shared_screen.vol_slider_p.value>AUDIO_MIN_VOLUME_DB:
                shared_screen_p.audio_control_volume(self.parent.parent.ids.shared_screen.vol_slider_p-1)
            else:
                print("Reached Min Volume")


###################################################################################################################


class DVDScreen(Screen):
    def __init__(self, **kwargs):
        super(DVDScreen, self).__init__(**kwargs)
        self.dvd_button_set=False

    def on_enter(self):
        def initialize_dvd_button(dt):
            self.ids.ondvd.state='down'
            dvd_source_dvd()

        if not self.dvd_button_set:
            Clock.schedule_once(initialize_dvd_button)
            self.dvd_button_set=True

    def dvd_play(self):
        control._write(rb'i', rb'9', DVD_VCR_PLAY_TYPE.encode(
            'utf-8'), DVD_VCR_PLAY.encode('utf-8'))
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'DVD-VCR-PLAY')

    def dvd_stop(self):
        control._write(rb'i', rb'9', DVD_VCR_STOP_TYPE.encode(
            'utf-8'), DVD_VCR_STOP.encode('utf-8'))
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'DVD-VCR-STOP')

    def dvd_pause(self):
        control._write(rb'i', rb'9', DVD_VCR_PAUSE_TYPE.encode(
            'utf-8'), DVD_VCR_PAUSE.encode('utf-8'))
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'DVD-VCR-PAUSE')

    def dvd_rew(self):
        control._write(rb'i', rb'9', DVD_VCR_REW_TYPE.encode(
            'utf-8'), DVD_VCR_REW.encode('utf-8'))
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'DVD-VCR-REW')

    def dvd_ff(self):
        control._write(rb'i', rb'9', DVD_VCR_FF_TYPE.encode(
            'utf-8'), DVD_VCR_FF.encode('utf-8'))
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'DVD-VCR-FF')

    def dvd_vcr_eject(self):
        control._write(rb'i', rb'9', DVD_VCR_EJECT_TYPE.encode(
            'utf-8'), DVD_VCR_EJECT.encode('utf-8'))
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'DVD-VCR-EJECT')

    def normal_control_buttons(self):
        self.ids.play.state='normal'
        self.ids.stop.state='normal'
        self.ids.pause.state='normal'
        self.ids.rewind.state='normal'
        self.ids.ff.state='normal'
        self.ids.eject.state='normal'

    def dvdvcr_dvd_selected(self, state):
        dvd_source_dvd()
        self.normal_control_buttons()
        if state == 'normal':
            self.ids.ondvd.state='down'
            insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'DVD-VCR-DVD')

    def dvdvcr_vcr_selected(self, state):
        dvd_source_vcr()
        self.normal_control_buttons()
        if state == 'normal':
            self.ids.onvcr.state='down'
            insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'DVD-VCR-DVD')

    def change_screens(self):
        self.parent.parent.ids.screen_management_volume.current='help_tools_screen'
        self.parent.parent.ids.screen_management.current='help_screen'


###################################################################################################################


class DocCamScreen(Screen):
    def doc_cam_off(self, state):
        control._write(rb's', rb'3', rb's', DOC_CAM_OFF.encode('utf-8'))
        if state == 'normal':
            self.ids.offdoccam.state='down'
            insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'DOC-CAM-OFF')

    def doc_cam_on(self, state):
        control._write(rb's', rb'3', rb's', DOC_CAM_ON.encode('utf-8'))
        control._write(rb's', rb'3', rb's',
                       DOC_CAM_SOURCE_PRESENTER.encode('utf-8'))
        if state == 'normal':
            self.ids.ondoccam.state='down'
            insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'DOC-CAM-ON')

    def change_screens(self):
        self.parent.parent.ids.screen_management_volume.current='help_tools_screen'
        self.parent.parent.ids.screen_management.current='help_screen'


###################################################################################################################


class LaptopScreen(Screen):
    def __init__(self, **kwargs):
        super(LaptopScreen, self).__init__(**kwargs)
        self.laptop_button_set=False

    def on_enter(self):
        if IS_LAPTOP_HDMIT_AVAILABLE == 'false':
            self.ids.laptop_hdmi.disabled=True

        def initialize_laptop_button(dt):
            if CURRENT_LAPTOP_SRC == 'vga':
                self.ids.laptop_vga.state='down'

            else:
                self.ids.laptop_hdmi.state='down'

        if not self.laptop_button_set:
            Clock.schedule_once(initialize_laptop_button)
            self.laptop_button_set=True

    def laptop_hdmi_src(self, state):
        global CURRENT_LAPTOP_SRC
        CURRENT_LAPTOP_SRC='hdmi'

        audio_mixer_select_projector()
        projector_laptop_hdmi()
        if state == 'normal':
            self.ids.laptop_hdmi.state='down'
            insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'LAPTOP_HDMI')

    def laptop_vga_src(self, state):
        global CURRENT_LAPTOP_SRC
        CURRENT_LAPTOP_SRC='vga'

        audio_mixer_select_laptop()
        projector_laptop_vga()
        if state == 'normal':
            self.ids.laptop_vga.state='down'
            insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'LAPTOP_VGA')

    def set_laptop_vga_state(self):
        self.ids.laptop_vga.state='normal'

    def set_laptop_hdmi_state(self):
        self.ids.laptop_hdmi.state='normal'

    def change_screens(self):
        self.parent.parent.ids.screen_management_volume.current='help_tools_screen'
        self.parent.parent.ids.screen_management.current='help_screen'


###################################################################################################################


class CableTvScreen(Screen):
    def cable_chan_up_selected(button):
        cable_chan_up()
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'CABLE-CHAN-UP')

    def cable_chan_down_selected(button):
        cable_chan_down()
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'CABLE-CHAN-DOWN')

    def cable_chan_zero_selected(button):
        cable_chan_zero()
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'CABLE-CHAN-ZERO')

    def cable_chan_one_selected(button):
        cable_chan_one()
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'CABLE-CHAN-ONE')

    def cable_chan_two_selected(button):
        cable_chan_two()
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'CABLE-CHAN-TWO')

    def cable_chan_three_selected(button):
        cable_chan_three()
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'CABLE-CHAN-THREE')

    def cable_chan_four_selected(button):
        cable_chan_four()
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'CABLE-CHAN-FOUR')

    def cable_chan_five_selected(button):
        cable_chan_five()
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'CABLE-CHAN-FIVE')

    def cable_chan_six_selected(button):
        cable_chan_six()
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'CABLE-CHAN-SIX')

    def cable_chan_seven_selected(button):
        cable_chan_seven()
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'CABLE-CHAN-SEVEN')

    def cable_chan_eight_selected(button):
        cable_chan_eight()
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'CABLE-CHAN-EIGHT')

    def cable_chan_nine_selected(button):
        cable_chan_nine()
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'CABLE-CHAN-NINE')

    def change_screens(self):
        self.parent.parent.ids.screen_management_volume.current='help_tools_screen'
        self.parent.parent.ids.screen_management.current='help_screen'

    def change_screens_listing(self):
        self.parent.parent.ids.screen_management_volume.current='cable_guide_tools_screen'
        self.parent.parent.ids.screen_management.current='cable_tv_guide_screen'


###################################################################################################################


class CableTvGuideScreen(Screen):
    def on_enter(self):
        self.ids.scrollview_tv_guide.scroll_y=1


###################################################################################################################


class CableTvPresetsScreen(Screen):
    def cable_mtvu_selected(self):
        Clock.schedule_once(lambda dt: cable_chan_three())
        Clock.schedule_once(lambda dt: cable_chan_one(), 2.4)
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS,
                          'CABLE-PRESETS-MTVU')

    def cable_campus_channel_selected(self):
        Clock.schedule_once(lambda dt: cable_chan_three())
        Clock.schedule_once(lambda dt: cable_chan_two(), 2.4)
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS,
                          'CABLE-PRESETS-CAMPUS-CHANNEL')

    def cable_pbs_selected(self):
        cable_chan_one()
        Clock.schedule_once(lambda dt: cable_chan_two(), .7)
        Clock.schedule_once(lambda dt: cable_chan_one(), 1)
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'CABLE-PRESETS-PBS')

    def cable_nbc_selected(self):
        cable_chan_one()
        Clock.schedule_once(lambda dt: cable_chan_seven(), .7)
        Clock.schedule_once(lambda dt: cable_chan_one(), 1)
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'CABLE-PRESETS-NBC')

    def cable_abc_selected(self):
        cable_chan_two()
        Clock.schedule_once(lambda dt: cable_chan_zero(), .7)
        Clock.schedule_once(lambda dt: cable_chan_one(), 1)
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'CABLE-PRESETS-ABC')

    def cable_cbs_selected(self):
        cable_chan_four()
        Clock.schedule_once(lambda dt: cable_chan_nine(), .7)
        Clock.schedule_once(lambda dt: cable_chan_two(), 1)
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'CABLE-PRESETS-CBS')

    def cable_fox_selected(self):
        cable_chan_five()
        Clock.schedule_once(lambda dt: cable_chan_five(), .7)
        Clock.schedule_once(lambda dt: cable_chan_one(), 1)
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'CABLE-PRESETS-FOX')

    def cable_cnn_selected(self):
        cable_chan_two()
        Clock.schedule_once(lambda dt: cable_chan_four(), .7)
        Clock.schedule_once(lambda dt: cable_chan_one(), 1)
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'CABLE-PRESETS-CNN')

    def cable_cspan_selected(self):
        cable_chan_two()
        Clock.schedule_once(lambda dt: cable_chan_seven(), .7)
        Clock.schedule_once(lambda dt: cable_chan_one(), 1)
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS,
                          'CABLE-PRESETS-CSPAN')

    def cable_espnu_selected(self):
        cable_chan_three()
        Clock.schedule_once(lambda dt: cable_chan_seven(), .7)
        Clock.schedule_once(lambda dt: cable_chan_two(), 1)
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS,
                          'CABLE-PRESETS-ESPNU')

    def cable_syfy_selected(self):
        cable_chan_four()
        Clock.schedule_once(lambda dt: cable_chan_six(), .7)
        Clock.schedule_once(lambda dt: cable_chan_one(), 1)
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS,
                          'CABLE-PRESETS-SYFY')

    def cable_disney_selected(self):
        cable_chan_six()
        Clock.schedule_once(lambda dt: cable_chan_two(), .7)
        Clock.schedule_once(lambda dt: cable_chan_two(), 1)
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS,
                          'CABLE-PRESETS-DISNEY')

    def cable_twc_selected(self):
        cable_chan_five()
        Clock.schedule_once(lambda dt: cable_chan_three(), .7)
        Clock.schedule_once(lambda dt: cable_chan_one(), 1)
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'CABLE-PRESETS-TWC')

    def cable_tlc_selected(self):
        cable_chan_five()
        Clock.schedule_once(lambda dt: cable_chan_four(), .7)
        Clock.schedule_once(lambda dt: cable_chan_one(), 1)
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'CABLE-PRESETS-TLC')

    def cable_hist_selected(self):
        cable_chan_five()
        Clock.schedule_once(lambda dt: cable_chan_four(), .7)
        Clock.schedule_once(lambda dt: cable_chan_two(), 1)
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS,
                          'CABLE-PRESETS-HISTORY')

    def cable_disc_selected(self):
        cable_chan_five()
        Clock.schedule_once(lambda dt: cable_chan_seven(), .7)
        Clock.schedule_once(lambda dt: cable_chan_one(), 1)
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS,
                          'CABLE-PRESETS-DISCOVERY')

    def cable_ngc_selected(self):
        cable_chan_five()
        Clock.schedule_once(lambda dt: cable_chan_six(), .7)
        Clock.schedule_once(lambda dt: cable_chan_two(), 1)
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'CABLE-PRESETS-NGC')

    def cable_ae_selected(self):
        cable_chan_three()
        Clock.schedule_once(lambda dt: cable_chan_nine(), .7)
        Clock.schedule_once(lambda dt: cable_chan_one(), 1)
        insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'CABLE-PRESETS-AE')


###################################################################################################################


class WifiCollabScreen(Screen):
    def on_enter(self):
        self.ids.scrollview_wifi_guide_ios.scroll_y=1
        self.ids.scrollview_wifi_guide_android.scroll_y=1
        self.ids.scrollview_wifi_guide_win.scroll_y=1

    def change_screens(self):
        self.parent.parent.ids.screen_management_volume.current='help_tools_screen'
        self.parent.parent.ids.screen_management.current='help_screen'


###################################################################################################################


class RebootScreen(Screen):
    pass


###################################################################################################################


class EmailScreen(Screen):
    pass


###################################################################################################################


class HeaderScreen(Screen):
    pass


###################################################################################################################


class HelpScreen(Screen):
    def on_leave(self):
        self.ids.howto_video1.seek(0)
        self.ids.howto_video1.state='stop'


###################################################################################################################


class SharedScreen(Screen):
    vol_slider_p=ObjectProperty(None)
    vol_audio_mute_p=ObjectProperty(None)
    vol_video_mute_p=ObjectProperty(None)
    VOLUME_LEVEL_BEFORE_MUTE=STARTUP_VOLUME_LEVEL

    def audio_control_volume(self, value):
        control._write(rb'p', rb'1', rb'p', str(int(value)).encode('utf-8'))

    def projector_video_mute(self, state):
        if state == 'down':
            control._write(rb's', rb'2', rb's',
                           PROJECTOR_MUTE_ON.encode('utf-8'))
            insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'VIDEO-MUTE')

            self.parent.parent.ids.screen_management.main_screen_p.dvd_p.disabled=True
            self.parent.parent.ids.screen_management.main_screen_p.cable_p.disabled=True
            self.parent.parent.ids.screen_management.main_screen_p.pc_p.disabled=True
            self.parent.parent.ids.screen_management.main_screen_p.doccam_p.disabled=True
            self.parent.parent.ids.screen_management.main_screen_p.wificollab_p.disabled=True
            self.parent.parent.ids.screen_management.main_screen_p.laptop_p.disabled=True

        elif state == 'normal':
            control._write(rb's', rb'2', rb's',
                           PROJECTOR_MUTE_OFF.encode('utf-8'))
            insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'VIDEO-UNMUTE')

            if IS_CABLE_AVAILABLE == 'true':
                self.parent.parent.ids.screen_management.main_screen_p.cable_p.disabled=False

            if IS_DOC_CAM_AVAILABLE == 'true':
                self.parent.parent.ids.screen_management.main_screen_p.doccam_p.disabled=False

            self.parent.parent.ids.screen_management.main_screen_p.dvd_p.disabled=False
            self.parent.parent.ids.screen_management.main_screen_p.pc_p.disabled=False
            self.parent.parent.ids.screen_management.main_screen_p.wificollab_p.disabled=False
            self.parent.parent.ids.screen_management.main_screen_p.laptop_p.disabled=False

    def audio_mute(self, state):
        if state == 'down':
            self.VOLUME_LEVEL_BEFORE_MUTE=self.ids.vol_slider.value

            self.vol_slider_p.value=0

            if ARDUINO_IS_MIXER == 'true':
                audio_mixer_select_mute()

            insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'AUDIO-MUTE')

        elif state == 'normal':
            self.ids.vol_slider.value=self.VOLUME_LEVEL_BEFORE_MUTE

            if ARDUINO_IS_MIXER == 'true':
                audio_mixer_select_unmute()

            insertButtonPress(SESSIONID, USERNAME, IP_ADDRESS, 'AUDIO-UNMUTE')


###################################################################################################################


class HelpToolsScreen(Screen):
    def on_enter(self):
        self.ids.help_ip_address.text=IP_ADDRESS

    def change_screens(self):
        self.parent.parent.ids.screen_management_volume.current='shared_vol_screen'
        self.parent.parent.ids.screen_management.current='main'

    def rebootipi(self):
        self.parent.parent.ids.screen_management.current='rebootscreen'
        reset_devices()
        insertButtonPress(SESSIONID, USERNAME, HOSTNAME, 'REBOOT')
        Clock.schedule_once(lambda dt: os.system('reboot now'), 10)

    def emailhelpdesk(self):
        self.parent.parent.ids.screen_management.current='emailscreen'
        sender='do-not-reply@uis.edu'
        recipients=EMAIL_HELPDESK_RECIPIENTS.split(",")

        msg=MIMEMultipart('alternative')
        msg['Subject']="Help Needed in Classroom"
        msg['From']=sender
        msg['To']=", ".join(recipients)

        htmltext="An issue requiring immediate attention was reported from this classroom control unit: <b>" + HOSTNAME + \
                 "</b><br><br>Please call the classroom phone immediately.<br><a target='_blank' href='http://go.uis.edu/classphones'>http://go.uis.edu/classphones</a><br><br>Reported by " + USERNAME + " from " + IP_ADDRESS

        part1=MIMEText(htmltext, 'html')

        msg.attach(part1)

        s=smtplib.SMTP('smtp.uisad.uis.edu')
        s.sendmail(sender, recipients, msg.as_string())
        s.quit()

        insertButtonPress(SESSIONID, USERNAME, HOSTNAME, 'EMAIL-HELPDESK')


###################################################################################################################


class CableGuideToolsScreen(Screen):
    def change_screens(self):
        self.parent.parent.ids.screen_management_volume.current='shared_vol_screen'
        self.parent.parent.ids.screen_management.current='cable_tvscreen'


###################################################################################################################


class RootWidget(BoxLayout):
    pass


###################################################################################################################
class SpeakScreen():
    dvd_p=ObjectProperty(None)
    cable_p=ObjectProperty(None)
    pc_p=ObjectProperty(None)
    doccam_p=ObjectProperty(None)
    wificollab_p=ObjectProperty(None)
    laptop_p=ObjectProperty(None)
    shared_screen_p=ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.button_set=False

    def on_enter(self):
        def initialize_buttons(dt):
            self.ids.off.state='down'
            Clock.schedule_once(lambda dt: self.disable_buttons(), 1)
            Clock.schedule_interval(lambda dt: self.update_clock(), 1)

            self.ids.off.disabled=True

        if not self.button_set:
            Clock.schedule_once(initialize_buttons)
            self.button_set=True

            scheduler=BackgroundScheduler()
            scheduler.add_job(self.scheduled_reboot, 'cron',
                              day_of_week='mon-sun', hour=2, minute=0, misfire_grace_time=1000)
            scheduler.start()

    Window.clearcolor=OFF_WHITE

    for group in ('source', 'power'):
        for widget in ToggleButton.get_widgets(group):
            widget.allow_no_selection=False


    def disable_buttons(self):
        self.ids.dvd.disabled=True
        self.ids.cable.disabled=True
        self.ids.pc.disabled=True
        self.ids.doccam.disabled=True
        self.ids.wificollab.disabled=True
        self.ids.laptop.disabled=True
        self.parent.parent.ids.shared_screen.vol_slider_p.disabled=True
        self.parent.parent.ids.shared_screen.audio_mute_p.disabled=True
        self.parent.parent.ids.shared_screen.video_mute_p.disabled=True

    def enable_buttons(self):
        if IS_CABLE_AVAILABLE == 'true':
            self.ids.cable.disabled=False

        if IS_DOC_CAM_AVAILABLE == 'true':
            self.ids.doccam.disabled=False

        self.ids.dvd.disabled=False
        self.ids.pc.disabled=False
        self.ids.wificollab.disabled=False
        self.ids.laptop.disabled=False
        self.parent.parent.ids.shared_screen.vol_slider_p.disabled=False
        self.parent.parent.ids.shared_screen.audio_mute_p.disabled=False
        self.parent.parent.ids.shared_screen.video_mute_p.disabled=False

    def disable_off(self):
        self.ids.off.disabled=True

    def disable_on(self):
        self.ids.on.disabled=True

    def blink(self, element, duration, rate):
        def set_style(dt):
            if element.state == 'normal':
                element.state='down'
            elif element.state == 'down':
                element.state='normal'

        def clean_up(dt):
            Clock.unschedule(set_style)

            element.state='down'

            self.ids.on.disabled=False
            self.ids.off.disabled=False

        self.ids.on.disabled=True
        self.ids.off.disabled=True

        Clock.schedule_interval(set_style, rate)
        Clock.schedule_once(clean_up, duration)






    def system_on(self):
        self.ids.off.state='normal'
        self.parent.parent.ids.shared_screen.vol_slider_p.value=float(
            STARTUP_VOLUME_LEVEL)
        self.blink(self.ids.on, 25, .5)

        Clock.schedule_once(lambda dt: self.ids.pc.trigger_action(), 15)
        projector_on()
        wakeup_pc()
        wakeup_pc()

        set_random_variable()

        Clock.schedule_once(lambda dt: projector_hdmi1(), 15)

        if ARDUINO_IS_MIXER == 'true':
            Clock.schedule_once(lambda dt: audio_mixer_select_unmute(), 17)

        Clock.schedule_once(lambda dt: self.enable_buttons(), 25)
        Clock.schedule_once(lambda dt: self.disable_on(), 28)

    def system_off(self):
        self.blink(self.ids.off, 15, .5)
        reset_devices()
        self.parent.parent.ids.shared_screen.vol_slider_p.value=0

        self.ids.dvd.state='normal'
        self.ids.cable.state='normal'
        self.ids.pc.state='normal'
        self.ids.doccam.state='normal'
        self.ids.wificollab.state='normal'
        self.ids.laptop.state='normal'

        Clock.schedule_once(lambda dt: insertButtonPress(
            SESSIONID, USERNAME, IP_ADDRESS, 'OFF'), 1)
        Clock.schedule_once(lambda dt: initialize_global_vars(), 2)

        Clock.schedule_once(lambda dt: self.disable_buttons(), 1)
        Clock.schedule_once(lambda dt: self.disable_off(), 18)

    def volume_up(self):
        if self.parent.parent.ids.shared_screen.vol_slider_p.value < AUDIO_MAX_VOLUME_DB:
            shared_screen_p.audio_control_volume(self.parent.parent.ids.shared_screen.vol_slider_p + 1)
        else:
            print("Reached Max Volume")

    def volume_down(self):
        if self.parent.parent.ids.shared_screen.vol_slider_p.value > AUDIO_MIN_VOLUME_DB:
            shared_screen_p.audio_control_volume(self.parent.parent.ids.shared_screen.vol_slider_p - 1)
        else:
            print("Reached Min Volume")




def get_audio():
    r  = sr.Recognizer()
    with sr.Microphone() as source:
        audio  = r.listen(source)
    try:
        value = r.recognize_google(audio)
        return value
    except sr.UnknownValueError as e:
        return e
def voice1():
    s = SpeakScreen()
    while(1):
        voice = get_audio()
        if voice == "projector on":
            s.system_on()
        if voice == "projector off":
            s.system_off()
        if voice == "volume up":
            s.volume_up()
        if voice == "volume down":
            s.volume_down()



main = Thread(target = voice1)
main.setDaemon(True)
main.start()



class MainApp(App):
    # These variables are available to the .kv file (Ex: app.MIN_VOLUME_DB)
    MIN_VOLUME_DB=float(AUDIO_MIN_VOLUME_DB)
    MAX_VOLUME_DB=float(AUDIO_MAX_VOLUME_DB)


    def build(self):
        control.on_event('configuration', 0, 'online', self.initialize)
        return RootWidget()

    def initialize(self):
        if ARDUINO_IS_MIXER == 'true':
            digital_config()

        projector_config()
        doc_cam_config()





if __name__ == '__main__':
    try:
        MainApp().run()
    except KeyboardInterrupt:
        raise
    finally:
        control.__exit__(None, None, None)
