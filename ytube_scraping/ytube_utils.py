import re
import datetime
from dateutil.relativedelta import relativedelta
from dateutil import parser
def text_trim(input):
    step_1= re.sub('\n', ' ', input)
    step_2= re.sub('\t', ' ', step_1)
    step_3= re.sub(r'[^\w]', ' ', step_2.lower())
    step_4= re.sub(r"'", ' ', step_3)
    step_5= step_4.replace('  ', ' ')
    step_6= step_5.strip()
    result= re.compile('[\ㄱ-ㅎ\ㅏ-ㅣ]+').sub('',step_6)
    return result
def vid_date_convert(input):
    date=  cmt_date_convert(input) if '공개' in input or '시작' in input else parser.parse(input[-12:]).strftime("%Y-%m-%d %H:%M:%S")
    return date
def cmt_date_convert(input):
    now= datetime.datetime.now()
    date_calculated= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_int= int(re.sub('[^0-9]', '', input))
    if '년' in input:
        date_calculated= (now - relativedelta(years=date_int)).strftime("%Y-%m-%d %H:%M:%S")
    elif '개월' in input:
        date_calculated= (now - relativedelta(months=date_int)).strftime("%Y-%m-%d %H:%M:%S")
    elif '주' in input:
        date_calculated= (now - relativedelta(days=date_int*7)).strftime("%Y-%m-%d %H:%M:%S")
    elif '일' in input:
        date_calculated= (now - relativedelta(days=date_int)).strftime("%Y-%m-%d %H:%M:%S")
    elif '시간' in input: 
        date_calculated= (now - relativedelta(hours=date_int)).strftime("%Y-%m-%d %H:%M:%S")
    elif '분' in input: 
        date_calculated= (now - relativedelta(minutes=date_int)).strftime("%Y-%m-%d %H:%M:%S")
    elif '초' in input: 
        date_calculated= (now - relativedelta(seconds=date_int)).strftime("%Y-%m-%d %H:%M:%S")
    return date_calculated
def count_convert(input):
    count_calculated= 0
    count_int= 0 if input == '' or '요' in input else float(re.sub('[^0-9.]', '', input))
    if '천' in input:
        count_calculated= int(count_int * 1000)
    elif '만' in input:
        count_calculated= int(count_int * 10000)
    elif input == '' or '아요':
        count_calculated= count_int
    else:
        count_calculated= int(input)
    return count_calculated
def addslashes(input):
    d = {'"': '\\"', "'": "\\'", "\0": "\\\0", "\\": "\\\\"}
    return ''.join(d.get(i, i) for i in input)
term_dict = {'시': 'AQ', '일': 'Ag', '주': 'Aw','달': 'BA', '연': 'BQ'}