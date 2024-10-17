from flask import Flask, render_template, request, redirect,flash
from flask import session
import sqlite3
app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'  # It's important to ensure that the secret key remains a secret that cannot be easily guessed.

conn= sqlite3.connect('user.db')
conn.execute(f'CREATE TABLE IF NOT EXISTS users (id INTEGER NOT NULL PRIMARY KEY autoincrement, username VARCHAR NOT NULL UNIQUE, '
                'password TEXT)')
conn.commit()



@app.route('/')
def home():

    print(session)
    return render_template("home.html") # Add you dashboard here



@app.route('/register', methods=['GET', 'POST'])
def register():
    message = 'Enter a username and password'
    if request.method == 'POST':
        # Print the form data to the console
        for key, value in request.form.items():
            print(f'{key}: {value}')

        # Can get name of the user from database here
        user_name = request.form['user_name']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if confirm_password == password:
            try:
                conn = sqlite3.connect('user.db')
                data = (user_name, password)
                conn.execute(f'INSERT INTO users (username, password) VALUES (?,?)', data)
                conn.commit()
                return redirect('/login')
            except sqlite3.IntegrityError and sqlite3.OperationalError:
                flash(f'this user already exists, try a different one')
                return render_template('register.html')
        else:
            placeholder="Must be the same as password"
            return render_template('register.html',placeholder=placeholder)

    else:
        return render_template("register.html", message=message)


# login page
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        # Print the form data to the console
        for key, value in request.form.items():
            print(f'{key}: {value}')
            username = request.form['username']
            password = request.form['password']
            print(session)
            # Can get name of the user from database here
            conn = sqlite3.connect('user.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM users WHERE username = {username} AND password = {password}")
            result = cursor.fetchone()

            global logged_in

            if result:
                session['username'] = request.form['username']
                logged_in=True
                flash(f'you have successfully logged in, {username}')
                return render_template('home.html',logged_in=logged_in)
            else:
                logged_in = False
                flash(f'invalid information given')
                return render_template('login.html')

    return render_template("login.html")


@app.route('/profile', methods=['GET','POST'])
def profile():
    global logged_in
    username = session['username']
    print(session)

    return render_template('profile.html',username=username,logged_in=logged_in)

@app.route('/logout')
def logout():
    global logged_in
    logged_in=False
    session.pop('username',None)
    flash(f'you have logged out')
    print('logged out')
    print(session)
    return redirect('/login')

global logged_in
logged_in=False
if __name__ == '__main__':
    app.run(debug=True)