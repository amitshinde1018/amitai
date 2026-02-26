from flask import Flask, render_template, request, redirect, session
import sqlite3, bcrypt

app = Flask(__name__)
app.secret_key = 'secret123'
DB = 'users.db'

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, username TEXT, email TEXT, password TEXT, role TEXT DEFAULT 'member')''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pw = request.form['password']
        conn = sqlite3.connect(DB)
        user = conn.execute('SELECT * FROM users WHERE email=?', (email,)).fetchone()
        conn.close()
        if user and bcrypt.checkpw(pw.encode(), user[3].encode()):
            session['user'] = user[1]
            session['email'] = user[2]
            session['role'] = user[4] if user[4] else 'member'
            return redirect('/dashboard')
        return render_template('login.html', error='Wrong email or password')
    return render_template('login.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        pw = bcrypt.hashpw(request.form['password'].encode(), bcrypt.gensalt()).decode()
        conn = sqlite3.connect(DB)
        conn.execute('INSERT INTO users (username, email, password, role) VALUES (?,?,?,?)', (username, email, pw, 'member'))
        conn.commit()
        conn.close()
        return redirect('/login')
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    return render_template('dashboard.html', username=session['user'], role=session.get('role'))

@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect('/login')
    return render_template('profile.html', username=session['user'], email=session['email'])

@app.route('/admin')
def admin():
    if 'user' not in session:
        return redirect('/login')
    if session.get('role') != 'admin':
        return redirect('/dashboard')
    conn = sqlite3.connect(DB)
    users = conn.execute('SELECT id, username, email, role FROM users').fetchall()
    conn.close()
    return render_template('admin.html', users=users, username=session['user'])

@app.route('/admin/delete/<int:user_id>')
def delete_user(user_id):
    if session.get('role') != 'admin':
        return redirect('/dashboard')
    conn = sqlite3.connect(DB)
    conn.execute('DELETE FROM users WHERE id=?', (user_id,))
    conn.commit()
    conn.close()
    return redirect('/admin')

@app.route('/admin/make_admin/<int:user_id>')
def make_admin(user_id):
    if session.get('role') != 'admin':
        return redirect('/dashboard')
    conn = sqlite3.connect(DB)
    conn.execute('UPDATE users SET role=? WHERE id=?', ('admin', user_id))
    conn.commit()
    conn.close()
    return redirect('/admin')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    init_db()
   app.run(host='0.0.0.0', port=10000)