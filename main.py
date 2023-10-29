from flask import Flask, render_template, request, url_for, redirect, make_response, session
import sqlite3
import library.tokens as tokens




connection = sqlite3.connect("data/users.db", check_same_thread=False)
cursor = connection.cursor()

app = Flask(__name__)
key = 'PUTIN_BOMBA_WZRIW_CHECHNYA'
app.secret_key = key




@app.route('/registercss')
def registercss():
    return render_template('css/register.css')



@app.route('/maincss')
def maincss():
    return render_template('main.css')
@app.route('/nicepagecss')
def nicepagecss():
    return render_template('nicepage.css')
@app.route('/')
def main():
    return render_template('main.html')

@app.route('/exit')
def exit():
    token = session.get('token')
    if not token:
        return redirect(url_for('register'))
    else:
        for key in list(session.keys()):
            session.pop(key)
        return redirect(url_for('register'))



@app.route('/changename', methods = ['POST', 'GET'])
def changename():
    token = session.get('token')
    if not token:
        return redirect(url_for('register'))
    else:
        if request.method == 'POST':
            user = request.form['n']
            cursor.execute("UPDATE oauth SET name = '{}' WHERE token = '{}'".format(user, token))
            connection.commit()
            return redirect(url_for('account'))
        else:
            return render_template('changename.html')
@app.route('/account')
def account():
    token = session.get('token')
    if not token:
        return redirect(url_for('register'))
    else:
        name = cursor.execute("SELECT name FROM oauth WHERE token = '{}'".format(token)).fetchone()[0]
        return render_template('account.html', name = name)


@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        user = request.form['u']
        password = request.form['p']
        token = tokens.generate_token(user, password)
        cursor.execute("SELECT mail FROM oauth WHERE token = '{}'".format(token))
        data = cursor.fetchone()
        if data is None:
            cursor.execute(f"INSERT INTO oauth VALUES('{user}', '{token}')")
            connection.commit()
            session['token'] = token
            return redirect(url_for('account'))
        else:
            session['token'] = token
            return redirect(url_for('account'))
    else:
        token = session.get('token')
        if not token:
            return render_template('register.html')
        else:
            return redirect(url_for('account'))

if __name__ == '__main__':
    app.run(port=80)