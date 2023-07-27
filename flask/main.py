from flask import Flask, request, render_template
import firebase_admin
from firebase_admin import credentials, firestore
import os

# Use a service account.
cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/list")
def list_data():
    # Fetch all document IDs in the 'devices' collection
    device_ids = [doc.id for doc in db.collection("devices").stream()]

    data = []

    # Fetch data from each device
    for device_id in device_ids:
        doc = db.collection("devices").document(device_id).get()
        if doc.exists:
            # Append a dict containing the device ID and its data
            data.append({device_id: doc.to_dict()})
        else:
            print(f"No such document {device_id}!")

    return render_template("list.html", data=data)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
