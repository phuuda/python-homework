import json
import codecs
import re
from collections import Counter

class Word:
    def __init__(self, text = '', count = 0, max_lex = '', max_gr = ''):
        self.text = text
        self.count = count
        self.max_lex = max_lex
        self.max_gr = max_gr

def create(**obj_values):
    new = Word()
    vars(new).update(obj_values)
    return new

data, w_data, marked_data, words = [], [], [], []

with codecs.open('python_mystem.json', 'rU', 'utf-8') as f:
    for line in f:
        data.append(json.loads(line)) # loads decodes 1 json object

for x in data:
    if 'analysis' in x:
        w_data.append(x)

# element in marked_data = [w_form, w_razbors, w_pos, w_lex]

for y in w_data:
    w_form = y['text']
    w_form = w_form.lower()
    w_pos, w_lex = [], []
    w_razbors = len(y['analysis'])
    
    for z in y['analysis']:
        for k, v in z.items():
            if k == 'gr': # extract POS
                m = v
                pos1 = re.findall('(.*?)=', m)
                if pos1:
                    for n in pos1:
                        if ',' in n:
                            pos = re.findall('(.*?),', n)
                            if pos:
                                w_pos.append(pos[0])
                                
                        if ',' not in n:
                            w_pos.append(n)

            if k == 'lex': # extract LEX
                w_lex.append(v)
                
    item = [w_form, w_razbors, w_pos, w_lex]
    if not marked_data:
        marked_data.append(item)

    i = 0
    if marked_data:           
        for line in marked_data:
            if line[0] == w_form:
                if w_razbors:
                    line[1] += w_razbors
                if w_pos:
                    for l in w_pos:
                        line[2].append(l)
                if w_lex:
                    for p in w_lex:
                        line[3].append(p)
                i += 1
                        
        if i == 0:
            marked_data.append(item)

                     
for el in marked_data:
    pos_count, lex_count = Counter(el[2]), Counter(el[3])
    
    if pos_count:
        el[2] = pos_count.most_common(1)[0][0]
    if not pos_count:
        el[2] = ''

    if lex_count:
        el[3] = lex_count.most_common(1)[0][0]
    if not lex_count:
        el[3] = ''

    x = create(text = el[0], count = el[1], max_lex = el[3], max_gr = el[2])
    words.append(x)


print(len(words))

for word in words:
    print(word.text)
    print(word.count)
    print(word.max_lex)
    print(word.max_gr)
    print('\n')


    
    
