from flask import Flask, render_template, request, redirect, session
import pyodbc

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Kết nối đến cơ sở dữ liệu
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-IA1SF1L6\\HUANPC;DATABASE=Bakery')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        phoneNumber = request.form['phoneNumber']
        email = request.form['email']
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Account (phoneNumber, email, username, password) VALUES (?, ?, ?, ?)", (phoneNumber, email, username, password))
        conn.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Account WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        if user:
            session['username'] = username
            return redirect('/')
        else:
            return 'Login failed. Invalid username or password.'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)