from flask import request, Flask, jsonify

app = Flask(__name__)


@app.route("/hello/<name>", methods = ["GET"])
def hello(name):
    greeting = "Hello {}!".format(name)
    return jsonify(greeting)


@app.route("/api/new_patient", methods = ["POST"])
def new_patient():
    # Places a new patient into the database
    patient = request.get_json()
    result = make_new_patient(patient)
    return jsonify(result)


@app.route("/api/heart_rate", methods = ["POST"])
def heart_rate():
    # Sets the current heart rate for a given patient (also needs a time?)
    print(1)


@app.route("/api/status/<patient_id>", methods = ["GET"])
def status(patient_id):
    # Tells whether the patient is tachycardic or not and gives
    # the time of the previous recording
    print(1)


@app.route("/api/heart_rate/<patient_id>", methods = ["GET"])
def heart_rate_full(patient_id):
    # Returns all previous heart rate measurements for the patient
    print(1)


@app.route("/api/heart_rate/average/<patient_id>", methods = ["GET"])
def heart_rate_average(patient_id):
    # Gives the average of all of the patient's HR data
    print(1)


@app.route("/api/heart_rate/interval_average", methods = ["POST"])
def interval_average():
    # Gives average heart rate since the given time
    print(1)


def make_new_patient(patient):
    uniqueid = patient["patient_id"]
    return uniqueid


if __name__ == "__main__":
    app.run(host = "127.0.0.1")
