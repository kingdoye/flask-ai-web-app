from flask import Flask, render_template, request
import numpy as np
import tensorflow as tf
from datetime import datetime
import math

app = Flask(__name__)

# Load the trained model
model = tf.keras.models.load_model("FINALYEAR_model.h5", compile=False)

# Function to convert time (HH:MM) to sin and cos components
def encode_time(time_str):
    try:
        dt = datetime.strptime(time_str, "%H:%M")
        minutes = dt.hour * 60 + dt.minute
        angle = 2 * math.pi * (minutes / 1440)  # 1440 minutes in a day
        return math.sin(angle), math.cos(angle)
    except:
        return 0, 1  # default fallback (midnight)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        inputs = []
        for i in range(1, 7):
            power = float(request.form[f"power{i}"])
            anomaly = float(request.form.get(f"anomaly{i}", 0))
            time_str = request.form.get(f"time{i}", "00:00")
            sin_t, cos_t = encode_time(time_str)
            inputs.append([power, anomaly, sin_t, cos_t])

        input_array = np.array(inputs).reshape(1, 6, 4)

        prediction = model.predict(input_array)
        predicted_power = prediction[0][0]  # or prediction[0] depending on model

        return render_template("result.html", prediction=predicted_power)

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
