import re
import json
from src.utils.xlsGetter import get_xls, clear_xls

template = {
    'weeks': ['一', '二', '三', '四', '五', '六', '日'],
    'lessons': ['1/2', '3/4/5', '6/7', '8/9/10', '11/12', '13/14'],
    'blank': [
        '// J! J! J!'
    ],
    'timeInfo': [
        ['// 08:00-08:45', '// 08:50-09:35'],
        ['// 09:50-10:35', '// 10:40-11:25', '// 11:30-12:15'],
        ['// 14:00-14:45', '// 14:50-15:35'],
        ['// 15:50-16:35', '// 16:40-17:25', '// 17:30-18:15'],
        ['// 19:00-19:45', '// 19:50-20:35'],
        ['// 20:00-21:25', '// 21:30-22:15']
    ]
}


def format_item(data):
    for i in range(len(data)):
        data[i] = data[i].replace('（', '(').replace('）', ')').replace('，', '/').replace(' ', '')
        data[i] = data[i].replace('[', ' [')
    for i in range(1, len(data) - 1):
        if '周' in data[i] and '周' != data[-1]:
            split = data[i].split('周')
            data[i] = '周'.join(split[:-1]) + '周'
            data[i + 1] = split[-1] + ' ' + data[i + 1]
    return [data[0], data[1], ' '.join(data[2:])]


def create_settings():
    table = get_xls()
    match = re.search('(^.+学期)', table.row_values(0)[0])
    template['courses'] = []
    template['header'] = match.group(1) + '个人课表'
    for i in range(2, table.nrows - 1):
        row = table.row_values(i)
        for j in range(2, len(row)):
            if row[j]:
                template['courses'].append({
                    'x': i - 2, 'y': j - 2,
                    'info': format_item(row[j].split('\n'))
                })
    template['footer'] = table.row_values(table.nrows - 1)[0]
    with open('../settings.json', 'w', encoding='utf-8') as file:
        json.dump(template, file, indent=4, ensure_ascii=False)
    clear_xls()
