from flask import request, Flask, jsonify
from PatientDatabase import Patient
import datetime

app = Flask(__name__)


@app.route("/hello/<name>", methods=["GET"])
def hello(name):
    greeting = "Hello {}!".format(name)
    return jsonify(greeting)


@app.route("/api/new_patient", methods=["POST"])
def new_patient():
    # Places a new patient into the database
    temp = request.get_json()
    patient = temp.json()
    createdpatient = make_new_patient(patient)
    return jsonify(createdpatient)


@app.route("/api/heart_rate", methods=["POST"])
def heart_rate():
    # Sets the current heart rate for a given patient (also needs a time?)
    # try:
    # Check if the patient_id exists and if not throw an error
    # except:
    temp = request.get_json()
    hrset = temp.json()
    set_heart_rate(hrset)



@app.route("/api/status/<patient_id>", methods=["GET"])
def status(patient_id):
    # Tells whether the patient is tachycardic or not and gives
    # the time of the previous recording

    status, time = getstatus(patient_id)
    return status, time


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def heart_rate_full(patient_id):
    # Returns all previous heart rate measurements for the patient
    hrlist = get_hr(patient_id)
    return hrlist


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def heart_rate_average(patient_id):
    # Gives the average of all of the patient's HR data
    hraverage = hr_averager(patient_id)
    return hraverage


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def interval_average():
    # Gives average heart rate since the given time
    temp = request.get_json()
    patienttime = temp.json()
    uniqueid = patienttime["patient_id"]
    desiredtime = patienttime["heart_rate_average_since"]
    index = index_finder(uniqueid, desiredtime)
    hr_averager(uniqueid, index)



def make_new_patient(patient):
    uniqueid = patient["patient_id"]
    newtemppatient = Patient(patient_id=uniqueid,
                             attending_email=patient["attending_email"],
                             user_age=patient["user_age"])
    newtemppatient.save()
    #print("Welcome Patient {}".format(uniqueid))
    for user in Patient.objects.raw({}):
        print(user.patient_id)
    return patient


def set_heart_rate(hrset):
    uniqueid = hrset["patient_id"]
    temppatient = Patient.objects.raw({"_id": uniqueid})
    # Place the given heart rate in the heart rate list
    fullhrlist = temppatient.hrlist
    fulltimelist = temppatient.timelist
    temp = fullhrlist.append(hrset["heart_rate"])
    temppatient.hrlist = temp
    # Place the current time in the time list
    temp = fulltimelist.append(datetime.datetime.now())
    temppatient.timelist = temp
    temppatient.save()

def getstatus(patient_id):
    temppatient = Patient.objects.raw({"_id": patient_id})
    allhr = temppatient.hrlist
    alltime = temppatient.timelist
    age = temppatient.user_age
    numhr = len(allhr)
    currenthr = allhr[numhr-1]
    currenttime = alltime[numhr-1]
    status = check_status(currenthr, age)

    return status, currenttime


def check_status(currenthr, age):
    status = "Not Tachycardic"
    if age == 1 or age == 2 and currenthr > 151:
        status = "Tachycardic"
    elif age == 3 or age == 4 and currenthr > 137:
        status = "Tachycardic"
    elif age >= 5 and age <= 7 and currenthr > 133:
        status = "Tachycardic"
    elif age >= 8 and age <= 11 and currenthr > 130:
        status = "Tachycardic"
    elif age >= 12 and age <= 15 and currenthr > 119:
        status = "Tachycardic"
    elif age > 15 and currenthr > 100:
        status = "Tachycardic"
    return status


def get_hr(patient_id):
    temppatient = Patient.objects.raw({"_id": patient_id})
    fullhrlist = temppatient.hrlist
    return fullhrlist


def hr_averager(patient_id, index = 0):
    total = 0
    fullhrlist = get_hr(patient_id)
    hrlen = len(fullhrlist)
    for val in range(index, hrlen-1):
        total = fullhrlist[val] + total
    hravg = total/hrlen
    return hravg


def index_finder(patient_id, time):
    index = 0
    temppatient = Patient.objects.raw({"_id": patient_id})
    fulltimelist = temppatient.timelist
    for x in fulltimelist:
        if time < x:
            break
        index += 1
    return index


if __name__ == "__main__":
    app.run(host = "127.0.0.1")
