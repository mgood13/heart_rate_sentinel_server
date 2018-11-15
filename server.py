from flask import request, Flask, jsonify
from PatientDatabase import Patient
import datetime

app = Flask(__name__)
masterlist = {}


@app.route("/hello/<name>", methods=["GET"])
def hello(name):
    greeting = "Hello {}!".format(name)
    return jsonify(greeting)


@app.route("/api/new_patient", methods=["POST"])
def new_patient():
    value = 1
    patient = request.get_json()
    message, checked = error_check(patient, value)
    if checked:
        createdpatient = make_new_patient(patient)
        return jsonify(createdpatient)
    else:
        return message


@app.route("/api/heart_rate", methods=["POST"])
def heart_rate():
    value = 2
    # Sets the current heart rate for a given patient
    hrset = request.get_json()
    message, checked = error_check(hrset, value)
    if checked:
        addtime = set_heart_rate(hrset)
        return jsonify("Heart Rate Added at {}".format(addtime))
    else:
        return message


@app.route("/api/status/<patient_id>", methods=["GET"])
def status(patient_id):
    value = 3
    # Tells whether the patient is tachycardic or not and gives
    # the time of the previous recording
    temppatient = {}
    temppatient["patient_id"] = patient_id
    message, checked = error_check(temppatient, value)
    if checked:
        currentstatus, time = getstatus(patient_id)
        printedresponse = "Patient is {}".format(currentstatus) +\
                          ". Measured at {}".format(time)
        print(printedresponse)
        return jsonify(printedresponse)
    else:
        return message


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def heart_rate_full(patient_id):
    value = 4
    # Returns all previous heart rate measurements for the patient
    hrlist = get_hr(patient_id)
    return hrlist


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def heart_rate_average(patient_id):
     value = 5
     # Gives the average of all of the patient's HR data
     hraverage = hr_averager(patient_id)
     return hraverage


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def interval_average():
    value = 6
    # Gives average heart rate since the given time
    temp = request.get_json()
    patienttime = temp.json()
    uniqueid = patienttime["patient_id"]
    desiredtime = patienttime["heart_rate_average_since"]
    index = index_finder(uniqueid, desiredtime)
    hr_averager(uniqueid, index)


def error_check(patient, value):
    keylist = []
    error = True
    # Places a new patient into the database
    alreadypatient = "Already Exists"
    uniqueid = patient["patient_id"]
    errormessage = ""

    for key in patient:
        keylist.append(key)

    if value == 1:
        expectedlist = ["patient_id", "attending_email", "user_age"]
    if value == 2:
        expectedlist = ["patient_id", "heart_rate"]
    if value == 3:
        try:
            if str(uniqueid) not in masterlist and value > 1:
                raise ValueError
        except ValueError:
            errormessage = jsonify("Patient does not exist")
            error = False
        if error:
            try:
                if not masterlist[str(uniqueid)].hrlist:
                    raise ValueError

            except ValueError:
                errormessage = jsonify("Patient has no recorded Heart Rate!")
                error = False

        return errormessage, error

    try:
        for i in expectedlist:
            if i not in keylist:
                raise AttributeError
    except AttributeError:
        errormessage = jsonify("{} value missing".format(i))
        error = False
    try:
        if str(uniqueid) in masterlist and value == 1:
            print("HELLO")
            raise ValueError
    except ValueError:
        errormessage = jsonify("Patient " + str(uniqueid) + " " + alreadypatient)
        error = False
    try:
        if str(uniqueid) not in masterlist and value > 1:
            raise ValueError
    except ValueError:
        errormessage = jsonify("Patient does not exist")
        error = False
    try:
        if "heart_rate" in keylist:
            if patient["heart_rate"] > 220 or  patient["heart_rate"] < 10:
                raise ValueError
    except ValueError:
        error = False
        errormessage = jsonify("Heart Rate is out of bounds")

    return errormessage, error


def make_new_patient(patient):
    uniqueid = patient["patient_id"]
    newtemppatient = Patient(patient_id=uniqueid,
                             attending_email=patient["attending_email"],
                             user_age=patient["user_age"],
                             hrlist=[],
                             timelist=[])
    # Hang onto this for if we get a database up and running
    # newtemppatient.save()
    masterlist[str(uniqueid)] = newtemppatient
    for key in masterlist:
        print(masterlist[key].patient_id)
    return patient


def set_heart_rate(hrset):
    uniqueid = hrset["patient_id"]
    temppatient = masterlist[str(uniqueid)]
    # Place the given heart rate in the heart rate list
    fullhrlist = temppatient.hrlist
    fulltimelist = temppatient.timelist
    temppatient.hrlist.append(hrset["heart_rate"])
    # Place the current time in the time list
    currenttime = datetime.datetime.now()
    temppatient.timelist.append(currenttime)
    return currenttime


def getstatus(patient_id):
    print(patient_id)
    print(type(patient_id))
    temppatient = masterlist[patient_id]
    allhr = temppatient.hrlist
    print("allhr")
    print(allhr)
    alltime = temppatient.timelist
    age = int(temppatient.user_age)
    currenthr = allhr[-1]
    currenttime = alltime[-1]
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
