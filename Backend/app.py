from flask import Flask, render_template, jsonify
import random
import time
import webbrowser
import threading

app = Flask(__name__)

start_time = time.time()
fixed_temp = round(random.uniform(33, 35), 2)

dehydrated_value = round(random.uniform(45, 54), 2)
hydrated_value = round(random.uniform(55, 75), 2)


@app.route("/")
def home():
    return render_template("index1.html")


@app.route("/get_status")
def get_status():

    elapsed_time = time.time() - start_time

    # ----------------------------
    # DIABETES LOGIC
    # ----------------------------
    if elapsed_time < 15:
        diabetes_status = "Normal"
        acetone = format(random.uniform(0.5, 1.5), ".6f")

    elif 15 <= elapsed_time < 27:
        diabetes_status = "Mild"
        acetone = format(random.uniform(1.6, 2.0), ".6f")

    else:
        diabetes_status = "Normal"
        acetone = format(random.uniform(0.5, 1.5), ".6f")

    # ----------------------------
    # Kidney Always Normal
    # ----------------------------
    kidney_status = "Normal"
    ammonia = format(random.uniform(0.0, 0.2), ".6f")

    # ----------------------------
    # HYDRATION LOGIC
    # ----------------------------
    if elapsed_time < 10:
        hydration_status = "Dehydrated"
        humidity = dehydrated_value

    elif 10 <= elapsed_time < 25:
        hydration_status = "Hydrated"
        humidity = hydrated_value

    else:
        hydration_status = "Dehydrated"
        humidity = dehydrated_value

    voc = round(random.uniform(100, 200), 2)
    temp = fixed_temp

    return jsonify({
        "diabetes": diabetes_status,
        "kidney": kidney_status,
        "hydration": hydration_status,
        "acetone": acetone,
        "ammonia": ammonia,
        "temp": temp,
        "humidity": humidity,
        "voc": voc
    })


# 🔥 Auto Open Browser
def open_browser():
    webbrowser.open("http://10.210.59.159:5000")


if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    app.run(host="10.210.59.159", port=5000, debug=True)