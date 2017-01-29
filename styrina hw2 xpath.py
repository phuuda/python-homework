# hw2 xpath -- Sofia Styrina

import lxml
from lxml import html
import requests
import re

class Professor:
    def __init__(self, surname = '', name = '', patronym = '',
                 jobs = {}, interests = [], phones = [], emails = []):
        self.surname = surname
        self.name = name
        self.patronym = patronym
        self.jobs = {}  # position + department
        self.interests = []
        self.phones = []
        self.emails = []

professors = []
page = requests.get('https://www.hse.ru/org/persons/?ltr=%D0%A4;udept=22726')  
tree = html.fromstring(page.content) # everything here

for person in tree.xpath('//div[@class="post person"]'):
    new_record = Professor()

#-----------------------------NAME-----------------------------
    full_name = person.xpath('.//div[@class="g-pic person-avatar-small2"]/@title')
    
    full_name = str(full_name)
    last_name = full_name.split()[0]
    last_name = last_name.replace("['", "")
    first_name = full_name.split()[1]
    c = full_name.count(' ')
    if c == 2:
        patronym_name = full_name.split()[2]
    else:
        patronym_name = 'N/A'
    patronym_name = patronym_name.replace("']", "")

    new_record.surname = last_name
    new_record.name = first_name
    new_record.patronym = patronym_name
#-----------------------------PHONES-----------------------------
    phone_nums = person.xpath('.//div[@class="l-extra small"]/span/text()')
    new_record.phones = phone_nums
#-----------------------------EMAILS-----------------------------
    email_list = person.xpath('.//div[@class="l-extra small"]/a/@data-at')
    a = ''
    for x in email_list:
        a += str(x)
    a = a.replace('"', '')
    a = a.replace(',', '')
    a = a.replace('[', '')
    a = a.replace(']', '')
    a = a.replace('-at-', '@')
    a = a.replace('.ru', '.ru ')        
    email_list = a.split(' ')
    email_list = [x for x in email_list if x != '']
    
    new_record.emails = email_list
#-----------------------------JOBS--------------------------------
    position_list = []
    positions = person.xpath('.//p[@class="with-indent7"]/span/text()')
    for x in positions:
        x = x.replace('\t','')
        x = x.replace('\n','')
        x = x.replace('\r', '')
        x = x.replace('/', '')
        x = x.replace(':', '')
        if x != '':
            position_list.append(x)
    
    dept_list = []
    for x in person.xpath('.//p[@class="with-indent7"]/span'):
        dept = x.xpath('.//a[@class="link"]/text()')
        dept_list.append(dept)

    if len(dept_list) != len(position_list):
        del position_list[-1]
    
    job_list = {}
    for x in range(len(dept_list)):
        job_list[position_list[x]] = dept_list[x]
        
    new_record.jobs = job_list
#-----------------------------INTERESTS-----------------------------
    interest_list = person.xpath('.//a[@class="tag"]/text()')
    new_record.interests = interest_list
    
    professors.append(new_record)
#----------------------------PRINT LIST-----------------------------    
for i in professors:
    print('фамилия: ' + i.surname)    
    print('имя: ' + i.name)
    print('отчество: ' + i.patronym)
    print('')
    
    for key, value in i.jobs.items():
        print('должность: ' + str(key))
        print('факультет: ' + str(value))
        print('')
    
    print('интересы:')
    for m in i.interests:
        print(m)
    print('')

    print('телефон:')
    for x in i.phones:
        print(x)
    print('')
    
    print('адрес почты:')
    for y in i.emails:
        print(y)
    print('------------------------------------------')
    print('')
