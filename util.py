
import datetime
from tts import synthesize_voice_play


def speak(text, gentle = True):
    if gentle:
        now = datetime.datetime.now()

        if now.hour < 6 or now.hour > 22:
            print(text)
            return

    synthesize_voice_play(text)
