import lxml
from lxml import etree
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

def teachers_with_etree(htmladdress): # feed me a webpage from whence to extract people
    page = requests.get(htmladdress)  
    root = etree.HTML(page.content)
    professors = []
    persons = root[1][1][3][2][1][0][2][1]

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
    return(professors)        

def teachers_with_xpath(htmladdress):
    professors = []
    page = requests.get(htmladdress)  
    tree = html.fromstring(page.content)
    
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
    return(professors)

professors1 = teachers_with_etree('https://www.hse.ru/org/persons/?ltr=%D0%A4;udept=22726')
professors2 = teachers_with_xpath('https://www.hse.ru/org/persons/?ltr=%D0%A4;udept=22726')
#----------------------------PRINT LIST-----------------------------    
for i in professors2:
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
