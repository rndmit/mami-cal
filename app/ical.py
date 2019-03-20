import arrow
from datetime import timedelta
from ics import Calendar, Event

import parser
from consts import lesson_time

TIMESTAMP_FORMAT = 'YYYY-MM-DD:HH-mm'
TIMEZONE = 'Europe/Moscow'

def build(data: dict):
    calendar = Calendar()

    for day in data.keys():
        for lesson in data[day].keys():
            for item in data[day][lesson]:
                print(item['subject']) #Just for debugging

                location = str()
                if len(item['auditories']) == 1:
                    location = item['auditories'][0]['title']
                else:
                    for i in item['auditories']:
                        location += (i['title'])
                
                df = arrow.get(item['date_from'] + ':' + lesson_time[lesson], TIMESTAMP_FORMAT).replace(days=(int(day) - 1))
                print(df)
                dt = arrow.get(item['date_to'] + ':' + lesson_time[lesson], TIMESTAMP_FORMAT)

                for r in arrow.Arrow.range('week', df, dt):
                    print(r.tzinfo)
                    calendar.events.add(Event(
                        name=item['subject'],
                        begin=r.replace(tzinfo=TIMEZONE),
                        duration=timedelta(minutes=90),
                        location=location,
                        description='Преподаватель: ' + item['teacher']
                    ))
    open('caricular.ics', 'w').writelines(calendar)

if __name__ == '__main__':
    build(parser.get_data('181-362'))