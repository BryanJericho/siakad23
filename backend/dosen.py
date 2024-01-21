from flask import Blueprint, request, render_template, jsonify, redirect, url_for, session, flash
from backend.db import db
from backend.auth import login_required
from database import data_dosen

dosenapp = Blueprint('dosenapp', __name__)

@dosenapp.route('/dosen')
@login_required
def dosen():
  return render_template ("dosen/dosen.html", data=data_dosen)


@dosenapp.route('/dosen/lihat/<nip>')
@login_required
def lihat_dosen(nip):
  data = {}
  for dosen in data_dosen:
    if dosen['nip'] == nip:
      data = dosen
  return render_template ("dosen/lihat.html", data=data)  