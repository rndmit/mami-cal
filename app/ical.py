import os
import arrow
from datetime import timedelta
from ics import Calendar, Event
from flask import current_app as app


TIMESTAMP_FORMAT = 'YYYY-MM-DD:HH-mm'
TIMEZONE = 'Europe/Moscow'
LESSON_TIME = {
    '1': '09-00',
    '2': '10-40',
    '3': '12-20',
    '4': '14-30',
    '5': '16-10',
    '6': '17-50',
    '7': '19-30',
}

# For representing positions in turple returned by items()
KEY = 0
DATA = 1

def build(data: dict):
    '''Builds a calendar from the dictionary

    Keyword arguments:
    data -- recieved from rasp.dmami.ru JSON
    '''
    calendar = Calendar()
    for day in data.items():                                                            # Проходим по каждому дню недели
        day_num = int(day[KEY])
        for lesson in day[DATA].items():                                                   # Проходим по каждой паре
            lesson_num = str(lesson[KEY])
            for item in lesson[DATA]:

                # Формируем таймстэмпы начала и конца текущей дисциплины с учетом времени начала пары
                df = arrow.get(item['date_from'] + ':' + LESSON_TIME[lesson_num], TIMESTAMP_FORMAT).replace(days=(day_num - 1))
                dt = arrow.get(item['date_to'] + ':' + LESSON_TIME[lesson_num], TIMESTAMP_FORMAT)

                # Проходим по всем числам от начала до конца с интервалом в неделю
                for r in arrow.Arrow.range('week', df, dt):
                    calendar.events.add(Event(
                            name = item['subject'],
                            begin = r.replace(tzinfo=TIMEZONE),
                            duration = timedelta(minutes=90),
                            location = ', '.join(i['title'] for i in item['auditories']),
                            description = item['type'] + '\n\nПреподаватель: ' + item['teacher']
                        ))

    return calendar

def save_to_ics(calendar: Calendar, filename: str):
    '''Saves calendar to ics-file with the specified name

    Keyword arguments:
    calendar -- Calendar object which must be saved into ics
    filename -- name without '.ics'
    '''
    with open(os.path.join(app.config['ICS_STORAGE_FOLDER'], filename), 'w') as file:
        file.writelines(calendar)