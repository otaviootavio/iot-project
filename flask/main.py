from flask import Flask, request, render_template
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.offline as pyo
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
    
    plots = temperature_plot()
    return render_template("list.html", data=data, plots = plots)


def temperature_plot():
    # Get current time and 24 hours ago
    now = datetime.now()
    one_day_ago = now - timedelta(hours=24)

    # Fetch all document IDs in the 'devices' collection
    device_ids = [doc.id for doc in db.collection('devices').stream()]

    plots = {}

    # Fetch data from each device
    for device_id in device_ids:
        # Get all log entries from the past 24 hours
        logs = (db.collection('devices')
                  .document(device_id)
                  .collection('logs')
                  .where('timestamp', '>', one_day_ago)
                  .stream())

        data = [log.to_dict() for log in logs]

        # Sort data by timestamp
        data.sort(key=lambda x: x['timestamp'])

        # Extract temperature and timestamp data
        timestamps = [x['timestamp'].strftime('%Y-%m-%d %H:%M:%S') for x in data]
        temperatures = [x['temperature'] for x in data]

        # Create plotly figure
        fig = go.Figure(data=go.Scatter(x=timestamps, y=temperatures))

        # Convert figure to HTML div string
        plot_div = pyo.plot(fig, output_type='div')

        # Map the device_id to the plot_div
        plots[device_id] = plot_div

    return plots

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
