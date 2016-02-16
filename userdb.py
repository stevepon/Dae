import sqlite3
import os
import webpageparts
from flask import Flask, url_for, request, session, redirect, render_template


app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path,'users.sqlite'),
    DEBUG=True,
    SECRET_KEY='go49ers'
))

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    return conn

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET','POST'])
def login():
    error = None

    cur = connect_db().cursor()

    if request.method=='POST':
        #password = request.form["password"]
        username = request.form['username']
        cur.execute('SELECT * from Users WHERE user LIKE ?', (username,))
        row = cur.fetchone()

        if row == None:
            error = 'User does not exist!'
        else:
            if request.form['password'] == row[1]:
                session['logged_in']=True
                return redirect(url_for('profile',username=username))
            else:
                error = 'Wrong password!'
        return render_template('login.html',error=error)
    else:
        return render_template('login.html')


@app.route('/users/<username>')
def profile(username):
    cur = connect_db().cursor()
    cur.execute('SELECT * from Users WHERE user LIKE ?', (username,))
    row = cur.fetchone()
    return render_template('profile.html',username=username,cats=row[2])


@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    return redirect(url_for('index'))


@app.route('/enter_webpage', methods=['GET','POST'])
def enter_webpage():
    if request.method == 'POST':
        url = request.form['url']
        session['url'] = url
        return redirect(url_for('webpage_data'))
    else:
        return render_template('enter_webpage.html')


@app.route('/webpage_data/')
def webpage_data():
    url = session['url']
    a = webpageparts.page_data(url)
    words = a[0]
    forms = len(a[1])
    fields = sum(a[1])
    external_links = a[2][1]
    links = a[2][0]
    print session
    return render_template('webpage_data.html',url=url,words=words,forms=forms,fields=fields,\
                           external_links=external_links,links=links)

if __name__ == '__main__':
    app.run()