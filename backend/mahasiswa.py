from flask import Blueprint, request, render_template, jsonify, redirect, url_for, session, flash
from backend.db import db, storage
from backend.auth import login_required
from firebase_admin import firestore
from datetime import datetime

mahasiswaapp = Blueprint('mahasiswaapp', __name__)

@mahasiswaapp.route('/mahasiswa')
@login_required
def mahasiswa():
  docs = db.collection('mahasiswa').order_by('created_at', direction=firestore.Query.DESCENDING).stream()
  data = [] 
  for doc in docs:
    s = doc.to_dict()
    s['id'] = doc.id
    data.append(s)
  # return jsonify(data)
  return render_template ("mahasiswa/mahasiswa.html", data=data)

@mahasiswaapp.route('/mahasiswa/tambah', methods =['GET', 'POST'])
@login_required
def tambah_mahasiswa():
  if request.method == "POST":
    data = {
      'created_at' : firestore.SERVER_TIMESTAMP,
      'nama_lengkap' : request.form['nama_lengkap'],
      'nim' : request.form['nim'],
      'tanggal_lahir' : request.form['tanggal_lahir'],
      'jurusan' : request.form['jurusan'],
      'status' : True 
    }
  
    if 'image' in request.files and request.files['image']:
            image = request.files['image']
            ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
            filename = image.filename
            lokasi = f"profil/{filename}"
            ext = filename.rsplit('.', 1)[1].lower()
            if ext in ALLOWED_EXTENSIONS:
                storage.child(lokasi).put(image)
                data['photoURL'] = storage.child(lokasi).get_url(None)
            else:
                flash("Foto tidak diperbolehkan", "danger")
                return redirect(url_for('.tambah'))
            db.collection('mahasiswa').document().set(data)
            flash('Berhasil Menambahkan data', 'success')
    # tangkap data dari request form
    # simpan ke database
    db.collection('mahasiswa').document().set(data)
    db.collection('counter').document('counter').set({'mahasiswa' : firestore.Increment(1)}, merge=True)
    flash("Berhasil Ditambahkan", 'success')

    return redirect(url_for('mahasiswaapp.mahasiswa'))
  
  return render_template ('/mahasiswa/tambah.html') 

@mahasiswaapp.route('/mahasiswa/lihat/<uid>')
@login_required
def lihat_mahasiswa(uid):
  data = db.collection('mahasiswa').document(uid).get().to_dict()

  return render_template ("mahasiswa/lihat.html", data=data)

@mahasiswaapp.route('/mahasiswa/edit/<uid>', methods=['GET', 'POST'])
@login_required
def edit_mahasiswa(uid):
  if request.method == 'POST':
    data = {
      'nama_lengkap' : request.form['nama_lengkap'],
      'nim' : request.form['nim'],
      'tanggal_lahir' : request.form['tanggal_lahir'],
      'jurusan' : request.form['jurusan'],
      'status' : True
    }
    db.collection('mahasiswa').document(uid).set(data)
    flash('Berhasil Diedit', 'success')
    # kalau document kosong itu dibuat baru tidak di edit
    return redirect(url_for('mahasiswaapp.mahasiswa'))
  
  data = db.collection('mahasiswa').document(uid).get().to_dict()
  return render_template ("mahasiswa/edit.html", data=data)

@mahasiswaapp.route('/mahasiswa/hapus/<uid>')
@login_required
def hapus_mahasiswa(uid):
  db.collection('mahasiswa').document(uid).delete()
  db.collection('counter').document('counter').set({'mahasiswa' : firestore.Increment(-1)}, merge=True)
  return redirect(url_for('mahasiswaapp.mahasiswa'))