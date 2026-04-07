from flask import Flask, jsonify, request, render_template, redirect, url_for
from collections import deque
import webbrowser
import threading

app = Flask(__name__)

# ---------------- History & Data ----------------
WINDOW = 10
history = {
    "acetone": deque(maxlen=WINDOW),
    "ammonia": deque(maxlen=WINDOW),
    "voc": deque(maxlen=WINDOW),
    "humidity": deque(maxlen=WINDOW)
}

sensor_data = {}

# ---------------- Helper Functions ----------------
def avg(values):
    return sum(values) / len(values) if values else None

def classify_health(data):
    acetone = data.get("acetone", 0)
    ammonia = data.get("ammonia", 0)
    voc = data.get("vocIndex", 0)
    humidity = data.get("humidity", 0)

    # Baselines
    base_acetone = avg(history["acetone"])
    base_ammonia = avg(history["ammonia"])
    base_voc = avg(history["voc"])

    delta_acetone = acetone - base_acetone if base_acetone else 0

    # ---------------- Diabetes ----------------
    if acetone < 5.0:
        diabetes = "Normal"
    elif 5.0 <= acetone < 7.0:
        diabetes = "Mild"
    else:
        diabetes = "Severe"

    # ---------------- Kidney ----------------
    if ammonia < 0.3:
        kidney = "Normal"
    elif 0.3 <= ammonia < 0.6:
        kidney = "Mild"
    else:
        kidney = "Severe"

    # ---------------- Hydration ----------------
    if humidity >= 59:
        hydration = "Hydrated"
    elif 45 <= humidity < 55:
        hydration = "Dehydrated"
    else:
        hydration = "Dehydrated"

    return diabetes, kidney, hydration, round(delta_acetone, 3)

# ---------------- Routes ----------------

# 🌟 Landing Page
@app.route('/')
def landing():
    return render_template('landing.html')

# 📊 Dashboard Page
@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

# 📡 Receive Sensor Data
@app.route('/data', methods=['POST'])
def receive_data():
    global sensor_data
    sensor_data = request.get_json()

    history["acetone"].append(sensor_data.get("acetone", 0))
    history["ammonia"].append(sensor_data.get("ammonia", 0))
    history["voc"].append(sensor_data.get("vocIndex", 0))
    history["humidity"].append(sensor_data.get("humidity", 0))

    diabetes, kidney, hydration, dA = classify_health(sensor_data)

    print(f"Received: {sensor_data} | ΔAcetone={dA} | Diabetes={diabetes}, Kidney={kidney}, Hydration={hydration}")

    return jsonify({"status": "ok"}), 200

# 📊 Send Data to Frontend
@app.route('/get_status', methods=['GET'])
def get_status():
    diabetes, kidney, hydration, dA = classify_health(sensor_data)

    return jsonify({
        "acetone": sensor_data.get("acetone", None),
        "ammonia": sensor_data.get("ammonia", None),
        "temperature": sensor_data.get("temperature", None),
        "humidity": sensor_data.get("humidity", None),
        "voc": sensor_data.get("vocIndex", None),
        "diabetes": diabetes,
        "kidney": kidney,
        "hydration": hydration
    })

# ---------------- Auto Open Browser ----------------
def open_browser():
    webbrowser.open_new("http://10.210.59.159:5000/")  # opens landing page

# ---------------- Run App ----------------
if __name__ == '__main__':
    threading.Timer(1, open_browser).start()
    app.run(host='0.0.0.0', port=5000, debug=True)