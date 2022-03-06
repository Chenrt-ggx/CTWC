import re
import json
from src.utils.xlsGetter import get_xls, clear_xls

template = {}

footer_match_list = [
    '(博雅课程).+?◇(.+?)◇(\d+-\d+)',
    '(实践与展示).+?◇(.+?)◇(\d+-\d+)'
]

course_name_format_list = [
    '体育\(\d+\)\((.+?)\d*?\)'
]

place_lesson_format_list = [
    '计算机教学实验中心\(新主楼([a-zA-Z0-9]+)\)'
]


def init_template():
    global template
    template = {
        'weeks': ['一', '二', '三', '四', '五', '六', '日'],
        'lessons': ['1/2', '3/4/5', '6/7', '8/9/10', '11/12', '13/14'],
        'blank': ['// J! J! J!'],
        'timeInfo': [
            ['// 08:00-08:45', '// 08:50-09:35'],
            ['// 09:50-10:35', '// 10:40-11:25', '// 11:30-12:15'],
            ['// 14:00-14:45', '// 14:50-15:35'],
            ['// 15:50-16:35', '// 16:40-17:25', '// 17:30-18:15'],
            ['// 19:00-19:45', '// 19:50-20:35'],
            ['// 20:40-21:25', '// 21:30-22:15']
        ],
        'courses': []
    }


def format_course_name(course_name):
    for i in course_name_format_list:
        match = re.search(i, course_name)
        if match is not None:
            course_name = match.group(1)
    return course_name


def format_teacher_time(teacher_time):
    teachers, times = [], [False for _ in range(20)]
    for i in teacher_time.split('周，'):
        split = i.split('[')
        if len(split) == 2:
            teacher, time = split[0].replace('|', ''), split[1]
            teachers.append(teacher)
            if re.search('(\d+)-(\d+)', time) is not None:
                match = re.search('(\d+)-(\d+)', time)
                for j in range(int(match.group(1)), int(match.group(2)) + 1):
                    times[j] = True
            elif re.search('(\d+)，(\d+)', time) is not None:
                match = re.search('(\d+)，(\d+)', time)
                times[int(match.group(1))] = times[int(match.group(2))] = True
            elif re.search('(\d+)', time) is not None:
                match = re.search('(\d+)', time)
                times[int(match.group(1))] = True
            else:
                print('parse \"' + time + '\" failed')
    teacher, time, start = '多名教师' if len(''.join(teachers)) > 7 else '/'.join(teachers), [], -1
    for i in range(len(times)):
        if times[i]:
            if start == -1:
                start = i
        else:
            if start != -1:
                time.append(str(i) if start == i - 1 else str(start) + '-' + str(i - 1))
            start = -1
    return teacher + ' [' + '/'.join(time) + ']周'


def format_place_lesson(place_lesson):
    for i in place_lesson_format_list:
        match = re.search(i + '(.*)', place_lesson)
        if match is not None:
            place_lesson = match.group(1) + match.group(2)
    return place_lesson.replace('，', '/')


def format_header(data):
    return re.search('(^.+学期)', data).group(1) + '个人课表'


def format_footer(data):
    result = []
    for i in footer_match_list:
        match = re.search(i, data)
        if match is not None:
            name, teacher, time = match.group(1), match.group(2), match.group(3)
            result.append(name + ' ' + teacher + ' [' + time + ']周')
    return '其它课程: ' + ' / '.join(result)


def format_item(data):
    for i in range(len(data)):
        data[i] = data[i].replace('（', '(').replace('）', ')').replace(' ', '')
    split = data[1].split('周')
    return [format_course_name(data[0]), format_teacher_time('周'.join(split[:-1])),
            format_place_lesson(' '.join([split[-1]] + data[2:]))]


def create_settings():
    init_template()
    table = get_xls()
    template['header'] = format_header(table.row_values(0)[0])
    template['footer'] = format_footer(table.row_values(table.nrows - 1)[0])
    for i in range(2, table.nrows - 1):
        row = table.row_values(i)
        for j in range(2, len(row)):
            if row[j]:
                template['courses'].append({
                    'x': i - 2, 'y': j - 2,
                    'info': format_item(row[j].split('\n'))
                })
    with open('../settings.json', 'w', encoding='utf-8') as file:
        json.dump(template, file, indent=4, ensure_ascii=False)
    clear_xls()
