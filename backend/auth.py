from flask import Blueprint, request, render_template, jsonify, redirect, url_for, session, flash
from backend.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

authapp = Blueprint('authapp', __name__)

@authapp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        data = {
            'username' : request.form['username'].replace(' ', '').lower(),
            'password' : request.form.get('password')
        }

        user = db.collection('users').document(data['username']).get().to_dict()


        # apakah ada user atau tidak
        if user:
            # apakah password sama dengan di database
            if check_password_hash(user['password'], data['password']):
                # simpan data usernya di dalam session
                session['user'] = user
                # ke halaman mahasiswa
                flash('Berhasil Login', 'success')
                # redirecit
                return redirect(url_for('mahasiswaapp.mahasiswa'))
            else:
                flash('Username/Password Salah', 'danger')
                return redirect(url_for('.login'))
        else:
            flash('Username/Password Salah', 'danger')
            return redirect(url_for('.login'))
        
    if 'user' in session:
        flash('Anda Sudah Login','warning')
        return redirect('mahasiswaapp.mahasiswa')

        
    return render_template('login.html')

@authapp.route('/register/', methods=['POST', 'GET'])
def register():
    # method post
    if request.method == 'POST':
        # ambil data dari form
        data = {
            'username' : request.form['username'].replace(' ','').lower(),
            'nama_lengkap' : request.form['nama_lengkap']
        }
        # cek apakah username sudah ada
        user = db.collection('users').document(data['username']).get().to_dict()

        if user:
            flash('Maaf Username Sudah Terdaftar', 'danger')
            return redirect(url_for('.register'))
        # cek apakah password sama
        if request.form['password'] != request.form['conf_password']:
            flash('Password Tidak Sama', 'danger')
            return redirect(url_for('.register'))
        elif len(request.form['password']) <=  3:
            flash('Password harus lebih dari 3 karakter', 'danger')
            return redirect(url_for('.register'))
        
        # enskripsi passwordnya
        data['password'] = generate_password_hash(request.form['password'])        
        # simpan data ke database
        db.collection('users').document(data['username']).set(data)
        # kasih flash
        flash('Berhasil Mendaftar, Silahkan Login', 'success')
        # kembali ke halaman login
        return redirect(url_for('.login'))
    return render_template('register.html')

@authapp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('.login'))

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            flash('Anda harus login', 'danger')
            return redirect(url_for('authapp.login'))
    return wrapper

@authapp.route('/dashboard')
@login_required
def dashboard():
    data = db.collection('counter').document('counter').get().to_dict()
    
    return render_template('index.html',data=data)