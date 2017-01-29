# hw2 etree - Sofia Styrina

import lxml
from lxml import etree
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
root = etree.HTML(page.content) # everything here

# /html/body/div[1]/div[4]/div[2]/div[2]/div/div[3]/div[2]/div[1]

persons = root[1][1][3][2][1][0][2][1] # <div class="post person"
# body/div/div/div/div/div/div/div

for person in persons:
    new_record = Professor()
#-----------------------------PHONES-----------------------------    
    phone_list = []
    lines = person[0][0].getchildren()
    for i in lines:
        if i.tag == 'span':
            phone_list.append(i.text)

    new_record.phones = phone_list
#-----------------------------EMAILS-----------------------------
    email_list = []
    lines = person[0][0].getchildren()
    for i in lines:
        if i.tag == 'a':
            email_list.append(i.get('data-at'))
    a = ''
    for i in email_list:
        a += str(i)
    a = a.replace('"', '')
    a = a.replace(',', '')
    a = a.replace('[', '')
    a = a.replace(']', '')
    a = a.replace('-at-', '@')
    a = a.replace('.ru', '.ru ')
    email_list = a.split(' ')
    email_list = [x for x in email_list if x != '']

    new_record.emails = email_list
#-----------------------------NAME-----------------------------
    interest_list = []
    job_list = {}
    x0 = person[0].getchildren()
    for x1 in x0:
        if x1 is not None:
            x2 = x1.getchildren() # [0][n]
            for x3 in x2:
                if x3 is not None:
                    x4 = x3.getchildren() # [0][n][m]
                    for x5 in x4:
                        if x5 is not None:
                            if x5.tag == 'a':
                                x6 = x5.getchildren()
                                for x7 in x6:
                                    if x7 is not None:
                                        if 'title' in x7.attrib:
                                            full_name = x7.get('title')
                                            last_name = full_name.split()[0] # last name
                                            first_name = full_name.split()[1] # first name
                                            c = full_name.count(' ')
                                            if c == 2:
                                                patronym_name = full_name.split()[2] # patronym
                                            else:
                                                patronym_name = 'N/A'

                                            new_record.surname = last_name
                                            new_record.name = first_name
                                            new_record.patronym = patronym_name
 #-----------------------------JOB POSITIONS-----------------------------                                               
                            if x5.tag == 'p':
                                x8 = x5.getchildren()
                                for x9 in x8:
                                    if x9 is not None:
                                        if x9.tag == 'span':
                                            position = x9.text
                                            position = re.sub('\t', '', position)
                                            position = re.sub('\n', '', position)
                                            position = re.sub('\r', '', position)
                                            position = re.sub(':', '', position)

#-----------------------------JOB DEPARTMENTS-----------------------------
                                            x10 = x9.getchildren() # inside 'span'

                                            departments = []
                                            for x11 in x10:
                                                if x11 is not None:
                                                    if x11.tag == 'a':
                                                        departments.append(x11.text)

                                            department = ''
                                            for x in departments:
                                                department += str(x)
                                                department += ' '

                                            job_list[position] = department

#-----------------------------INTERESTS-----------------------------
                            if x5.tag == 'div':
                                for x11 in x5.getchildren():
                                    if x11 is not None:
                                        interest_list.append(x11.text)
    new_record.jobs = job_list                                        
    new_record.interests = interest_list
    professors.append(new_record)

#----------------------------PRINT LIST----------------------------- 
for i in professors:
    print('фамилия: ' + i.surname)    
    print('имя: ' + i.name)
    print('отчество: ' + i.patronym)
    print('')
    
    for key, value in i.jobs.items():
        print('должность: ' + key)
        print('факультет: ' + value)
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
