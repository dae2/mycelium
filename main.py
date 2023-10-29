from flask import Flask, render_template, request, url_for, redirect, session
import sqlite3
import library.tokens as tokens

connection = sqlite3.connect("data/users.db", check_same_thread=False)
cursor = connection.cursor()
connectionu = sqlite3.connect("data/schoolu.db", check_same_thread=False)
cursoru = connectionu.cursor()
connections = sqlite3.connect("data/school.db", check_same_thread=False)
cursors = connections.cursor()


app = Flask(__name__)
key = 'PUTIN_BOMBA_WZRIW_CHECHNYA'
app.secret_key = key


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


@app.route('/changename', methods=['POST', 'GET'])
def changename():
    token = session.get('token')
    if not token:
        return redirect(url_for('register'))
    else:
        if request.method == 'POST':
            user = request.form['n']
            cursor.execute(
                "UPDATE oauth SET name = '{}' WHERE token = '{}'".format(user, token))
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
        premium = cursor.execute("SELECT premium FROM oauth WHERE token = '{}'".format(token)).fetchone()[0]
        if premium == 0:
            premium = 'daaaaaa'
        elif premium == 1:
            premium = 'Free'
        elif premium == 2:
            premium = 'Community'
        elif premium == 3:
            premium = 'Corporation'
        return render_template('account.html', name=name, premium=premium)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user = request.form['u']
        password = request.form['p']
        token = tokens.generate_token(user, password)
        cursor.execute("SELECT mail FROM oauth WHERE token = '{}'".format(token))
        data = cursor.fetchone()
        if data is None:
            if cursor.execute("SELECT mail FROM oauth WHERE mail = '{}'".format(user)).fetchone() is not None:
                return redirect(url_for('register'))
            cursor.execute(f"INSERT INTO oauth VALUES('{user}', '{user}', '{token}', 1, 'None')")
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

@app.route('/aboutus', methods=['GET'])
def aboutus():
    return render_template('abouts.html')


@app.route('/changepassword', methods=['GET', 'POST'])
def changepassword():
    if request.method == 'POST':
        password = request.form['p']
        token = session.get('token')
        user = cursor.execute("SELECT mail FROM oauth WHERE token = '{}'".format(token)).fetchone()[0]
        token = tokens.generate_token(user, password)
        cursor.execute("UPDATE oauth SET token = '{}' WHERE mail = '{}'".format(token, user))
        connection.commit()
        for key in list(session.keys()):
            session.pop(key)
        session['token'] = token
        return redirect(url_for('account'))
    else:
        return render_template('changepassword.html')

@app.route('/buytarif', methods=['GET', 'POST'])
def buytarif():
    if request.method == 'POST':
        tarif = request.form['choice']
        token = session.get('token')
        cursor.execute("UPDATE oauth SET premium = {} WHERE token = '{}'".format(tarif, token))
        connection.commit()
        return render_template('account.html')
    else:
        return render_template('buytarif.html')


@app.route('/addusers', methods=['GET', 'POST'])
def addusers():
    if request.method == 'POST':
        user = request.form['u']
        job = request.form['p']
        users = cursor.execute(f"SELECT name FROM oauth WHERE token = '{session.get('token')}'").fetchone()[0]
        num = cursoru.execute(f"SELECT max(num) FROM {users}").fetchone()[0]
        cursoru.execute(f"INSERT INTO {users} VALUES('{user}', '{job}', {num})")
        connectionu.commit()
        return redirect(url_for('school'))
    else:
        return render_template('addusers.html')






@app.route('/school', methods=['GET', 'POST'])
def school():
    listuser = ""
    name = cursor.execute("SELECT name FROM oauth WHERE token = '{}'".format(session.get('token'))).fetchone()[0]
    num = cursoru.execute(f"SELECT max(num) FROM {name}").fetchone()[0] + 1
    for i in range(1, num):
        names = cursoru.execute(f"SELECT name FROM {name} WHERE num = {i}").fetchone()[0]
        print(names)
        namess = cursoru.execute(f"SELECT job FROM {name} WHERE num = {i}").fetchone()[0]
        listuser = listuser + names + f"({namess})" + '\n'
    return render_template('myschool.html', listuser = listuser)



@app.route('/mycompany', methods=['GET', 'POST'])
def mycompany():
    if cursor.execute("SELECT school FROM oauth WHERE token = '{}'".format(session.get('token'))).fetchone()[0] == 'None':
        if request.method == 'GET':
            return render_template('school.html')
        else:
            school = request.form['n']
            token = session.get('token')
            user = cursor.execute("SELECT name FROM oauth WHERE token = '{}'".format(token)).fetchone()[0]
            cursor.execute("UPDATE oauth SET school = '{}' WHERE token = '{}'".format(school, token))
            cursors.execute(f"""CREATE TABLE IF NOT EXISTS {user}(
               name TEXT,
               job TEXT,
               test TEXT,
               num INT
               );
            """)
            cursoru.execute(f"""CREATE TABLE IF NOT EXISTS {user}(
               name TEXT,
               job TEXT,
               num INT
               );
            """)
            cursoru.execute(f"INSERT INTO {user} VALUES('None', 'None', 0)")
            cursors.execute(f"INSERT INTO {user} VALUES('None', 'None', 'None', 0)")
            connection.commit()
            connections.commit()
            connectionu.commit()
            return redirect(url_for('account'))
    else:
        return redirect(url_for('school'))


if __name__ == '__main__':
    app.run(port=80)
