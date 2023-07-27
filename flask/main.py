from flask import Flask, request, render_template
import firebase_admin
from firebase_admin import credentials, firestore
import os

# Use a service account.
cred = credentials.Certificate('serviceAccount.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/add', methods=['GET', 'POST'])
def add_data():
    if request.method == 'POST':
        data = {i: request.form[i] for i in request.form}
        db.collection('data').add(data)
    return render_template('form.html')

@app.route('/list')
def list_data():
    docs = db.collection('data').stream()
    data = [{doc.id: doc.to_dict()} for doc in docs]
    return render_template('list.html', data=data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
