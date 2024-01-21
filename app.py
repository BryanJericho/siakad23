from flask import Flask, request, render_template, jsonify, redirect, url_for, session, flash
from database import  data_dosen
from backend.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from backend.mahasiswa import mahasiswaapp
from backend.auth import authapp
from backend.jurusan import jurusanapp
from backend.dosen import dosenapp

# dari nama file import variabel yang sudah dibuat

app = Flask(__name__, static_folder='static', static_url_path='')
# saya memiliki static folder 
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'
# nama file

app.register_blueprint(mahasiswaapp)
app.register_blueprint(authapp)
app.register_blueprint(jurusanapp)
app.register_blueprint(dosenapp)

# routing 
@app.route('/')
def index():
    return redirect(url_for('authapp.login'))

if __name__ == '__main__':
  app.run(debug=True, port=5005)


# GET Dikirimkan lewat url
# POST DIkirimkan lewat belakang layar
