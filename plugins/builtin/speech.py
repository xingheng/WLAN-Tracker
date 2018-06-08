# -*- coding: utf-8 -*-
'''
Invoke the baidu text-to-speech to synthesis voice.
'''

import os
from tempfile import mkstemp
from sys import platform
from datetime import datetime
from logger import get_logger
from aip import AipSpeech
from pygame import mixer
from utils import *

logger = get_logger(__file__, F('.'))

TTS_APPID = None
TTS_APPKEY = None
TTS_SECRET = None


class Speech(object):
    __filepath = None

    def __init__(self, text, language='zh'):
        self.text = text
        self.language = language

    def play(self):
        global TTS_APPID, TTS_APPKEY, TTS_SECRET

        if not (TTS_APPID and TTS_APPKEY and TTS_SECRET):
            logger.error('Lack of app key configuration before speaking!')
            assert()

        client = AipSpeech(TTS_APPID, TTS_APPKEY, TTS_SECRET)

        result = client.synthesis(self.text, self.language, 1, {
            'vol': 15,  # 音量，取值0-15，默认为5中音量
            'pit': 0,  # 音调，取值0-9，默认为5中语调
            'per': 0,  # 发音人, 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫
            'cuid': platform
        })

        if isinstance(result, dict):
            logger.error(result)
            return False

        tmp_file = mkstemp('-tts-voice.mp3')
        self.__filepath = tmp_file[1]

        with open(self.__filepath, 'w') as f:
            f.write(result)

        return self.replay()

    def replay(self):
        if not self.__filepath:
            return False

        mixer.music.load(self.__filepath)
        mixer.music.play()
        while mixer.music.get_busy() == True:
            continue

        logger.info('Speak: %s', self.text)
        return True

    def __del__(self):
        if self.__filepath:
            os.remove(self.__filepath)


def speak(text, gentle=True):
    '''
        speech wrapper.
    '''
    if gentle and False:
        now = datetime.now()

        if now.hour < 6 or now.hour > 22:
            logger.info('Speak silent: %s', text)
            return

    if not initialize():
        logger.warning('Init failed!')

    Speech(text).play()


def initialize():
    path = get_data_file("baidu_tts.cfg", __file__)

    if os.path.exists(path):
        root = load_tuple_data(path)

        global TTS_APPID, TTS_APPKEY, TTS_SECRET
        TTS_APPID = root.keys.appid
        TTS_APPKEY = root.keys.appkey
        TTS_SECRET = root.keys.secret

        mixer.init()
        mixer.music.set_volume(1.0)
        return True

    with open(path, 'w') as f:
        f.write('''
{
    "keys": {
        "appid": null,
        "appkey": null,
        "secret": null
    }
}
        '''.strip())

    logger.info('Initialized a configuration file at %s', path)
    return False


if __name__ == "__main__":
    speak("Hello")
