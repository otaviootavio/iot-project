import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import numpy as np
import time

# Use a service account.
cred = credentials.Certificate('serviceAccount.json')

# Only initialize the app once.
try:
    firebase_admin.get_app()
except ValueError as e:
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Function to send data
def send_data(device_id, temperature, air_humidity, soil_humidity):
    current_time = datetime.now()

    # Update the main document for the device
    device_data = {
        'temperature': temperature,
        'air_humidity': air_humidity,
        'soil_humidity': soil_humidity,
        'last_updated': current_time
    }
    db.collection('devices').document(device_id).set(device_data, merge=True)

    # Add a new log entry
    log_data = {
        'temperature': temperature,
        'air_humidity': air_humidity,
        'soil_humidity': soil_humidity,
        'timestamp': current_time
    }
    db.collection('devices').document(device_id).collection('logs').add(log_data)

# You can call the function as follows:

# Define your factors for each of the parameters
temp_factor = 10
air_humidity_factor = 20
soil_humidity_factor = 30

# Choose the number of data points to generate
num_points = 100

for i in range(num_points):
    # Generate the data
    i_temp = i/ (num_points) * 2 * np.pi
    temperature = np.sin(i_temp) * temp_factor
    air_humidity = np.cos(i_temp) * air_humidity_factor
    soil_humidity = np.sin(i_temp) * np.cos(i_temp) * soil_humidity_factor

    # Send the data
    send_data('deviceID2', temperature, air_humidity, soil_humidity)

    # Wait for 1 second before sending the next set of data
    time.sleep(1)
