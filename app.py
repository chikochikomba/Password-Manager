from flask import Flask, render_template, request, redirect, url_for, session
from models import db, User, Password
from config import Config
from utilities import password_manager

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        master_password = request.form['master_password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return 'User already exists!'
        hashed = password_manager.hash_password(master_password)
        user = User(username=username, master_password_hash=hashed)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        master_password = request.form['master_password']
        user = User.query.filter_by(username=username).first()
        if user and password_manager.verify_password(master_password, user.master_password_hash):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    passwords = Password.query.filter_by(user_id=user_id).all()
    return render_template('dashboard.html', passwords=passwords, password_manager=password_manager)

@app.route('/add_password', methods=['GET', 'POST'])
def add_password():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        service_name = request.form['service_name']
        login = request.form['login']
        password = request.form['password']
        encrypted = password_manager.encrypt_password(password)
        new_pass = Password(service_name=service_name, login=login, password=encrypted, user_id=session['user_id'])
        db.session.add(new_pass)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_password.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
