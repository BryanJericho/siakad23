from flask import Blueprint, request, render_template, jsonify, redirect, url_for, session, flash
from backend.db import db
from backend.auth import login_required
from firebase_admin import firestore

jurusanapp = Blueprint('jurusanapp', __name__)

@jurusanapp.route('/jurusan')
@login_required
def jurusan():
  docs = db.collection('jurusan').stream()
  data = [] 
  for doc in docs:
    s = doc.to_dict()
    s['id'] = doc.id
    data.append(s)
  return render_template ("mahasiswa/jurusan.html", data = data)

@jurusanapp.route('/jurusan/tambah', methods =['GET', 'POST'])
@login_required
def tambah_jurusan():
  if request.method == "POST":
    data = {
      'jurusan' : request.form['jurusan']
    }
    db.collection('jurusan').document().set(data)
    db.collection('counter').document('counter').set({'jurusan' : firestore.Increment(1)}, merge=True)
    flash('Berhasil Menambahkan data', 'success')
    # tangkap data dari request form
    # simpan ke database

    return redirect(url_for('.jurusan'))
  
  return render_template ('/mahasiswa/tambah_jurusan.html') 

@jurusanapp.route('/jurusan/hapus/<uid>')
@login_required
def hapus_jurusan(uid):
  db.collection('jurusan').document(uid).delete()
  db.collection('counter').document('counter').set({'jurusan' : firestore.Increment(-1)}, merge=True)
  return redirect(url_for('jurusanapp.jurusan'))
