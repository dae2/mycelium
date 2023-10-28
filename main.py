from flask import Flask, render_template, request, url_for, redirect, make_response, session

app = Flask(__name__)
app.secret_key = 'WSSARMSHA'


@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/logincss')
def logincss():
    return render_template('css/login.css')


@app.route('/')
def main():
    return render_template('main.html')





@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['u']
        password = request.form['p']
        session['user_id'] = user
        return redirect(url_for('success', name=user))

    else:
        user_id = session.get('user_id')
        if not user_id:
            return render_template('login.html')
        else:
            return redirect(url_for('success', name=user_id))

if __name__ == '__main__':
    app.run(port=80)