from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from models import db, User, Password
from password_manager import PasswordManager
from utilities import generate_password
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    password_manager = PasswordManager(app.config['ENCRYPTION_KEY'])

    @app.route('/')
    def index():
        if 'user_id' in session:
            return redirect(url_for('dashboard'))
        return redirect(url_for('login'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash('Username already exists')
                return redirect(url_for('register'))
                
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            
            flash('Registration successful. Please login.')
            return redirect(url_for('login'))
            
        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                session['user_id'] = user.id
                return redirect(url_for('dashboard'))
            flash('Invalid username or password.')
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.clear()  # Changed from session.pop('user_id')
        return redirect(url_for('login'))

    @app.route('/dashboard')
    def dashboard():
        if 'user_id' not in session:
            return redirect(url_for('login'))

        user = User.query.get(session['user_id'])
        passwords = Password.query.filter_by(user_id=user.id).all()
        
        decrypted_passwords = []
        for p in passwords:
            try:
                decrypted_passwords.append({
                    'id': p.id,
                    'service': p.service,
                    'password': password_manager.decrypt_password(p.encrypted_password)
                })
            except:
                # Handle corrupted/invalid passwords
                continue

        return render_template('dashboard.html', passwords=decrypted_passwords)

    @app.route('/add-password', methods=['GET', 'POST'])
    def add_password():
        if 'user_id' not in session:
            return redirect(url_for('login'))

        if request.method == 'POST':
            service = request.form['service']
            password = request.form['password']

            user = User.query.get(session['user_id'])
            encrypted = password_manager.encrypt_password(password)
            new_password = Password(service=service, encrypted_password=encrypted, user_id=user.id)
            db.session.add(new_password)
            db.session.commit()
            flash('Password saved!')
            return redirect(url_for('dashboard'))

        return render_template('add_password.html')

    @app.route('/generate-password', methods=['POST'])
    def generate_password_route():
        length = int(request.form.get('length', 12))
        use_digits = request.form.get('digits') == 'on'
        use_symbols = request.form.get('symbols') == 'on'

        generated = generate_password(length=length, use_digits=use_digits, use_symbols=use_symbols)
        return jsonify({'password': generated})  # Return JSON instead of HTML

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)