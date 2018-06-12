# -*- coding: utf-8 -*-

import os
from datetime import datetime

from ..builtin import get_logger, speak, F, get_data_file, load_tuple_data

logger = get_logger(__file__, F('.'))
TOTAL_TERMS = None
REPORTED_TERMS = []


def solar_term_status():
    if not TOTAL_TERMS:
        initialize()

    now = datetime.now()
    hour = now.hour

    last_term, next_term = None, None
    last_term_delta, next_term_delta = 0, 0

    for term in TOTAL_TERMS:
        time = datetime.strptime(term.datetime, "%Y-%m-%d %H:%M")
        delta_seconds = (now - time).total_seconds()

        if delta_seconds > 0:
            if last_term_delta > delta_seconds or last_term_delta == 0:
                last_term = term
                last_term_delta = delta_seconds
        else:
            if next_term_delta < delta_seconds or next_term_delta == 0:
                next_term = term
                next_term_delta = delta_seconds

    text = u'节气提醒: '
    seconds_oneday = 24 * 60 * 60

    if last_term:
        text += u'今天是%s节气的第%d天.' % (last_term.name,
                                    last_term_delta / seconds_oneday)

    if next_term:
        text += u'距离下一个节气%s还有%d天.' % (next_term.name,
                                      abs(next_term_delta) / seconds_oneday)

    speak(text)


def solar_term_alarm():
    if not TOTAL_TERMS:
        initialize()

    now = datetime.now()
    hour = now.hour

    current_term = None

    for term in TOTAL_TERMS:
        time = datetime.strptime(term.datetime, "%Y-%m-%d %H:%M")
        delta_seconds = (now - time).total_seconds()

        if abs(delta_seconds) <= 10 * 60: # within 10 minutes
            current_term = term
            break

    if current_term:
        global REPORTED_TERMS

        if current_term.name not in REPORTED_TERMS:
            REPORTED_TERMS.append(current_term.name)
            text = u'节气提醒: '
            text += u'今日' + current_term.name + "."
            text += current_term.description

            speak(text)
        else:
            logger.info('Skip it as it\'s reported')


def initialize():
    path = get_data_file("terms.cfg", __file__)

    if os.path.exists(path):
        root = load_tuple_data(path)
        global TOTAL_TERMS
        TOTAL_TERMS = root.solar_terms
        return True

    with open(path, 'w') as f:
        f.write('''
{
    "solar_terms": [
        {
            "name": "立春",
            "datetime": "2018-02-04 08:00",
            "description": "风带雨逐西风，大地阳和暖气生。万物苏萌山水醒，农家岁首又谋耕。"
        }
    ]
}
        '''.strip())

    logger.info('Initialized a configuration file at %s', path)
    return False


if __name__ == "__main__":
    solar_term_status()
    solar_term_alarm()
