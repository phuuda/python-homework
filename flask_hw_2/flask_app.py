## LINK TO SITE: http://phuuda.pythonanywhere.com/

from flask import Flask
from flask import url_for, render_template, request, redirect
from pymystem3 import Mystem
from collections import Counter
import requests, operator, json

m = Mystem()
app = Flask(__name__)

def add_POS(text):
    result = []
    ana = m.analyze(text)
    for x in ana:
        if 'analysis' in x:
            result.append(x)
    return result

def get_verbs(pos_text):
    verbs = []
    for word in pos_text:
        if 'analysis' in word:
            if 'gr' in word['analysis'][0]:
                if 'V,' in word['analysis'][0]['gr']:
                    verbs.append(word)
    return verbs

def percent_verbs(verbs, pos_text):
    v_words = len(verbs)
    all_words = len(pos_text)
    v_percent = 100 * float(v_words) / all_words
    v_percent = float("{0:.2f}".format(v_percent))
    return(v_percent)    

def transitive_verbs(verbs):
    t_verbs = []
    for word in verbs:
        if 'пе=' in word['analysis'][0]['gr']:
            t_verbs.append(word)
    return(t_verbs)

def nesoversh_verbs(verbs):
    nes_verbs = []
    for word in verbs:
        if 'несов' in word['analysis'][0]['gr']:
            nes_verbs.append(word)
    return(nes_verbs)

def ordered_v_lexems(verbs):
    lexems = []
    for word in verbs:
        lex = word['analysis'][0]['lex']
        lexems.append(lex)
    counted_lex = Counter(lexems)
    sorted_lex = sorted(counted_lex.items(), key=operator.itemgetter(1), reverse=True)
    just_lex = []
    for el in sorted_lex:
        just_lex.append(el[0])
        
    return(just_lex)


# enter 2 open group ids
# return # of people in each group
# return # of people in both groups
# if closed group - return that


@app.route('/', methods=['get', 'post'])
def main_one():
    return render_template('index_page.html')

@app.route('/verb_page', methods=['get', 'post'])
def index():
    if request.form:
        text = request.form['text']
        
        pos_text = add_POS(text) #.replace('\n', '<br>')
        verbs = get_verbs(pos_text)
        v_quantity = len(verbs)
        v_percent = percent_verbs(verbs, pos_text)
        
        trans_verbs = transitive_verbs(verbs)
        t_verb_count = len(trans_verbs)
        intrans_verb_count = len(verbs) - len(trans_verbs)
        
        nes_verbs = nesoversh_verbs(verbs)
        nes_v_count = len(nes_verbs)
        sov_v_count = len(verbs) - len(nes_verbs)
        
        ordered_lexems = ordered_v_lexems(verbs)
            
        return render_template('verb_page.html', input=text, text=pos_text,
                               v_quantity=v_quantity, v_percent=v_percent, t_verb_count=t_verb_count,
                               intrans_verb_count=intrans_verb_count, nes_v_count=nes_v_count,
                               sov_v_count=sov_v_count, ordered_lexems=ordered_lexems)

    return render_template('verb_page.html')

@app.route('/vk_page', methods=['get', 'post'])

def vk_api():
    if request.form:
        client_id = '6010833'
        client_secret = 'WpWi6xJ68d73LwqSmHqU'
        grant_type = 'client_credentials'

        auth = 'https://oauth.vk.com/access_token?client_id='

        auth_response = requests.get(auth + client_id + '&client_secret=' + client_secret +
                                     '&v=5.63&grant_type=client_credentials')

        m = json.loads(auth_response.text)
        access_token = m['access_token']


        group_one = request.args['group_one']
        group_two = request.args['group_two']

        gr1_response = requests.get(api_link + method + '?id=' + group_one +
                            '&client_secret=' + access_token)

        gr2_response = requests.get(api_link + method + '?id=' + group_two +
                            '&client_secret=' + access_token)    

        group1 = gr1_response.text
        group2 = gr2_response.text

    
        return render_template('vk_page.html', group1=group1, group2=group2)
    
    return render_template('vk_page.html')    

if __name__ == '__main__':
    app.run(debug=True)
