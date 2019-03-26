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

def build(data: dict):
    '''Builds an calendar from the dictionary

        Args:
            data (dict) - recieved from rasp.dmami.ru JSON
        Returns: ics.Calendar
    '''
    calendar = Calendar()
    # TODO: Оптимизировать код
    for day in range(1, len(data)+1): #Проходим по каждому дню недели [1,6]
        for pair in range(1, len(data[str(day)])): # проходим по каждой паре
            pairs = data[str(day)][str(pair)]
            if len(pairs) > 0:
                # Собираем аудитории в location
                object_1 = pairs[0] # Содержит 1 элемент json`a
                location = ','.join(i['title'] for i in object_1['auditories'])
                # Формируем таймстэмпы начала и конца текущей дисциплины с учетом времени начала пары
                df = arrow.get(object_1['date_from'] + ':' + LESSON_TIME[str(pair)], TIMESTAMP_FORMAT).replace(days=(int(day) - 1))
                print(df)
                dt = arrow.get(object_1['date_to'] + ':' + LESSON_TIME[str(pair)], TIMESTAMP_FORMAT)
                # Проходим по всем числам от начала до конца с интервалом в неделю
                for r in arrow.Arrow.range('week', df, dt):
                    # Формируем событие и сразу добавляем его в календарь
                    calendar.events.add(Event(
                        name=object_1['subject'],
                        begin=r.replace(tzinfo=TIMEZONE),
                        duration=timedelta(minutes=90),
                        location=location,
                        description='Преподаватель: ' + object_1['teacher']
                    ))
    return calendar

def save_to_ics(calendar: Calendar, filename: str):
    '''Saves calendar to ics-file with the specified name

        Args:
            calendar: ics.Calendar - calendar object which should be saved to a file
            filename: str
        Returns: None
    '''
    open(os.path.join(app.config['ICS_STORAGE_FOLDER'], filename), 'w').writelines(calendar)
