# -*- coding: utf-8 -*-

import os
import sys
import tempfile
import config
from aip import AipSpeech
from pygame import mixer


def synthesize_voice(text, language='zh'):
    keys = config.KEYS
    client = AipSpeech(keys.baidu_tts_appid,
                       keys.baidu_tts_appkey,
                       keys.baidu_tts_secret)

    result = client.synthesis(text, language, 1, {
        'vol': 15,  # 音量，取值0-15，默认为5中音量
        'pit': 0,  # 音调，取值0-9，默认为5中语调
        'per': 0,  # 发音人, 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫
        'cuid': sys.platform
    })

    if not isinstance(result, dict):
        tmp_file = tempfile.mkstemp('-tts-voice.mp3')
        tmp_file_path = tmp_file[1]

        with open(tmp_file_path, 'w') as f:
            f.write(result)

        return tmp_file_path

    print result
    return None


def play_audio(filepath):
    mixer.init()
    mixer.music.load(filepath)
    mixer.music.set_volume(1.0)
    mixer.music.play()
    while mixer.music.get_busy() == True:
        continue


def synthesize_voice_play(text, language='zh'):
    path = synthesize_voice(text, language)

    if path:
        play_audio(path)
        os.remove(path)
        return True

    return False

