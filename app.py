from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from config import Config
from utils.database import Database, mysql
from utils.encryption import FileEncryption
from utils.auth import Authentication, login_required
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import io

app = Flask(__name__)
app.config.from_object(Config)
Database.init_app(app)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if not username or not email or not password:
            flash('All fields are required!', 'danger')
            return render_template('register.html')
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return render_template('register.html')
        if not Authentication.validate_email(email):
            flash('Invalid email format!', 'danger')
            return render_template('register.html')
        is_valid, error_msg = Authentication.validate_password(password)
        if not is_valid:
            flash(error_msg, 'danger')
            return render_template('register.html')
        if Database.get_user_by_username(username):
            flash('Username already exists!', 'danger')
            return render_template('register.html')
        if Database.get_user_by_email(email):
            flash('Email already registered!', 'danger')
            return render_template('register.html')
        
        password_hash = Authentication.hash_password(password)
        Database.create_user(username, email, password_hash)
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if not username or not password:
            flash('Please enter username and password!', 'danger')
            return render_template('login.html')
        user = Database.get_user_by_username(username)
        if not user or not Authentication.verify_password(user['password_hash'], password):
            flash('Invalid username or password!', 'danger')
            return render_template('login.html')
        session['user_id'] = user['id']
        session['username'] = user['username']
        flash(f'Welcome back, {user["username"]}!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_files = Database.get_user_files(session['user_id'])
    shared_files = Database.get_shared_files(session['user_id'])
    return render_template('dashboard.html', user_files=user_files, shared_files=shared_files)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected!', 'danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected!', 'danger')
            return redirect(request.url)
        if file and Config.allowed_file(file.filename):
            file_data = file.read()
            file_size = len(file_data)
            file_hash = FileEncryption.calculate_hash(file_data)
            encrypted_data, encryption_key = FileEncryption.encrypt_file(file_data)
            original_filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            encrypted_filename = f"{session['user_id']}_{timestamp}_{original_filename}.enc"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], encrypted_filename)
            with open(file_path, 'wb') as f:
                f.write(encrypted_data)
            file_id = Database.save_file_metadata(encrypted_filename, original_filename, file_hash, encryption_key, session['user_id'], file_size)
            Database.log_file_access(file_id, session['user_id'], 'upload', request.remote_addr)
            flash(f'File "{original_filename}" uploaded and encrypted successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('File type not allowed!', 'danger')
            return redirect(request.url)
    return render_template('upload.html')

@app.route('/download/<int:file_id>')
@login_required
def download(file_id):
    file_data = Database.get_file_by_id(file_id)
    if not file_data:
        flash('File not found!', 'danger')
        return redirect(url_for('dashboard'))
    if not Database.check_file_access(file_id, session['user_id']):
        flash('You do not have permission to access this file!', 'danger')
        return redirect(url_for('dashboard'))
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_data['filename'])
        with open(file_path, 'rb') as f:
            encrypted_data = f.read()
        encryption_key = file_data['encryption_key'].encode()
        decrypted_data = FileEncryption.decrypt_file(encrypted_data, encryption_key)
        if not FileEncryption.verify_hash(decrypted_data, file_data['file_hash']):
            flash('File integrity check failed!', 'danger')
            return redirect(url_for('dashboard'))
        Database.log_file_access(file_id, session['user_id'], 'download', request.remote_addr)
        return send_file(io.BytesIO(decrypted_data), as_attachment=True, download_name=file_data['original_filename'])
    except Exception as e:
        flash(f'Error downloading file: {str(e)}', 'danger')
        return redirect(url_for('dashboard'))

@app.route('/share/<int:file_id>', methods=['GET', 'POST'])
@login_required
def share(file_id):
    file_data = Database.get_file_by_id(file_id)
    if not file_data:
        flash('File not found!', 'danger')
        return redirect(url_for('dashboard'))
    if file_data['owner_id'] != session['user_id']:
        flash('You can only share your own files!', 'danger')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        share_username = request.form.get('username', '').strip()
        if not share_username:
            flash('Please enter a username!', 'danger')
            return render_template('shared.html', file=file_data)
        share_user = Database.get_user_by_username(share_username)
        if not share_user:
            flash('User not found!', 'danger')
            return render_template('shared.html', file=file_data)
        if share_user['id'] == session['user_id']:
            flash('You cannot share a file with yourself!', 'warning')
            return render_template('shared.html', file=file_data)
        try:
            Database.share_file(file_id, share_user['id'], session['user_id'])
            Database.log_file_access(file_id, session['user_id'], 'share', request.remote_addr)
            flash(f'File shared successfully with {share_username}!', 'success')
            return redirect(url_for('dashboard'))
        except:
            flash('File already shared with this user!', 'warning')
            return render_template('shared.html', file=file_data)
    return render_template('shared.html', file=file_data)

@app.route('/delete/<int:file_id>')
@login_required
def delete_file(file_id):
    file_data = Database.get_file_by_id(file_id)
    if not file_data:
        flash('File not found!', 'danger')
        return redirect(url_for('dashboard'))
    if file_data['owner_id'] != session['user_id']:
        flash('You can only delete your own files!', 'danger')
        return redirect(url_for('dashboard'))
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_data['filename'])
        if os.path.exists(file_path):
            os.remove(file_path)
        Database.log_file_access(file_id, session['user_id'], 'delete', request.remote_addr)
        Database.delete_file(file_id)
        flash('File deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting file: {str(e)}', 'danger')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)