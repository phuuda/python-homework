from flask import Flask
from flask import url_for, render_template, request, redirect

def create_file(f_name):
    f = open(f_name, 'w', encoding = 'utf-8')
    f.close()
    return 'file created'

create_file('results.txt')
app = Flask(__name__)

# CMD + Q TO KILL APPLICATION
# http://127.0.0.1:5000/hi


@app.route('/')
def initial():
    return render_template('cat_dog.html')

@app.route('/result')
def results():
    
    if request.args:
        name = request.args['name']
        cat = request.args['cat']
        dog = request.args['dog']
        
        f = open('results.txt', 'a', encoding = 'utf-8')
        f.write(name, cat, dog, '\n')
        data = f.read()
        f.close
        
        return render_template('results.html', name=name, cat=cat, dog=dog, data=data)
    return redirect(url_for('.hi'))

# http://127.0.0.1:5000/result?name=Sof&cats=cats
# Bad Request
# The browser (or proxy) sent a request that this server could not understand.

if __name__ == '__main__':
    app.run(debug=True)

