import arrow
from datetime import timedelta
from ics import Calendar, Event


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
    for day in data.keys():
        for lesson in data[day].keys():
            for item in data[day][lesson]:

                # Если аудиторий несколько - собираем их в одну строку
                location = str()
                if len(item['auditories']) == 1:
                    location = item['auditories'][0]['title']
                else:
                    for i in item['auditories']:
                        location += (i['title'])

                # Формируем таймстэмпы начала и конца текущей дисциплины с учетом времени начала пары
                df = arrow.get(item['date_from'] + ':' + LESSON_TIME[lesson], TIMESTAMP_FORMAT).replace(days=(int(day) - 1))
                print(df)
                dt = arrow.get(item['date_to'] + ':' + LESSON_TIME[lesson], TIMESTAMP_FORMAT)

                # Проходим по всем числам от начала до конца с интервалом в неделю
                for r in arrow.Arrow.range('week', df, dt):
                    # Формируем событие и сразу добавляем его в календарь
                    calendar.events.add(Event(
                        name=item['subject'],
                        begin=r.replace(tzinfo=TIMEZONE),
                        duration=timedelta(minutes=90),
                        location=location,
                        description='Преподаватель: ' + item['teacher']
                    ))

    return calendar

def save_to_ics(calendar: Calendar, filename: str):
    '''Saves calendar to ics-file with the specified name

        Args:
            calendar: ics.Calendar - calendar object which should be saved to a file
            filename: str
        Returns: None
    '''
    open('caricular.ics', 'w').writelines(calendar)