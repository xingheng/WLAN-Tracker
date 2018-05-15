# -*- coding: utf-8 -*-
'''
Invoke the baidu text-to-speech to synthesis voice.
'''

import os
from tempfile import mkstemp
from sys import platform
from datetime import datetime
from aip import AipSpeech
from pygame import mixer

TTS_APPID = None
TTS_APPKEY = None
TTS_SECRET = None


class Speech(object):
    __filepath = None

    def __init__(self, text, language='zh'):
        self.text = text
        self.language = language

    def play(self):
        if not (TTS_APPID and TTS_APPKEY and TTS_SECRET):
            assert()

        client = AipSpeech(TTS_APPID, TTS_APPKEY, TTS_SECRET)

        result = client.synthesis(self.text, self.language, 1, {
            'vol': 15,  # 音量，取值0-15，默认为5中音量
            'pit': 0,  # 音调，取值0-9，默认为5中语调
            'per': 0,  # 发音人, 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫
            'cuid': platform
        })

        if isinstance(result, dict):
            print result
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

        return True

    def __del__(self):
        if self.__filepath:
            os.remove(self.__filepath)


def speak(text, gentle=True):
    '''
        speech wrapper.
    '''
    if gentle:
        now = datetime.now()

        if now.hour < 6 or now.hour > 22:
            print(text)
            return

    Speech(text).play()


def setup(app):
    app.register_formatter(speak)
    path = app.get_generic_file("baidu_tts.cfg")

    if os.path.exists(path):
        root = app.load_tuple_data(path)

        global TTS_APPID, TTS_APPKEY, TTS_SECRET
        TTS_APPID = root.keys.appid
        TTS_APPKEY = root.keys.appkey
        TTS_SECRET = root.keys.secret

        mixer.init()
        mixer.music.set_volume(1.0)
        return

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

    print 'Initialized a configuration file at %s' % path
