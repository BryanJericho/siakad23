import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase

cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

config = {
  "apiKey": "AIzaSyAlWGo0ktZP1xtUZ4acXntqFGbHGPQUub0",
  "authDomain": "siakad-1cdd5.firebaseapp.com",
  "databaseURL": "https://siakad-1cdd5-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "siakad-1cdd5",
  "storageBucket": "siakad-1cdd5.appspot.com",
  "messagingSenderId": "680884422236",
  "appId": "1:680884422236:web:1764706eba111bbb334899"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()