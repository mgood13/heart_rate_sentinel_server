from flask import request, Flask, jsonify
from PatientDatabase import Patient
import datetime


app = Flask(__name__)
masterlist = {}


@app.route("/api/new_patient", methods=["POST"])
def new_patient():
    """ This function takes the input call and creates a new patient

    This function is a post function that is called from a separate program.
    It requires three different input values: patient_id, attending
    email, and patient age
    It first sends all of the new patients into the error checker function.
    Then the function returns either an error message or the created patient.

    :return createdpatient: A dictionary with the created patient
    :return message: An error message about how the patient creation failed
    """
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
    """ Function for adding heart rate values

    This function adds heart rate values for a given patient
    Similar to above this sends the patient for error checking and then will
    either add the heart rate or return an error message.

    :return goodmessage: Confirmation message for adding an HR value
    :return message: Error message about how the heart rate addition failed
    """
    value = 2
    # Sets the current heart rate for a given patient
    hrset = request.get_json()
    message, checked = error_check(hrset, value)
    goodmessage = "Heart Rate Added"
    if checked:
        addtime = set_heart_rate(hrset)
        return jsonify(goodmessage)
    else:
        return message


@app.route("/api/status/<patient_id>", methods=["GET"])
def status(patient_id):
    """ Function that determines if the patient has tachycardia

    This function takes in a patient ID number and then checks if their
    most recently recorded heart rate value is tachycardic depending upon
    their age. It also returns the time of that last measurement

    :param patient_id: The patient's ID number
    :return printedresponse: Patient status and time of last recording
    :return message: Error message about how the status checking failed
    """
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
        return jsonify(printedresponse)
    else:
        return message


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def heart_rate_full(patient_id):
    """Function that returns the entire heart rate list

    This function takes in the patient ID number and then returns the entire
    heart rate list for the patient.

    :param patient_id: The Patient's ID number
    :return printed response: String containing the full HR list
    :return message: Error message what went wrong getting the hr list
    """
    value = 4
    # Returns all previous heart rate measurements for the patient
    temppatient = {}
    temppatient["patient_id"] = patient_id
    message, checked = error_check(temppatient, value)
    if checked:
        hrlist = get_hr(patient_id)
        printedresponse = "Patient {}".format(patient_id) + \
                          " all heart rate values:" + str(hrlist)
        return jsonify(printedresponse)
    else:
        return message


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def heart_rate_average(patient_id):
    """Function that calculates the patient's average heart rate

    This function takes the patient's ID number and then returns the average
    heart rate or an error message

    :param patient_id: Patient's ID number
    :return hraverage: The patient's average heart rate
    :return message: Error message what went wrong averaging the heart rate
    """
    value = 5
    # Gives the average of all of the patient's HR data
    temppatient = {}
    temppatient["patient_id"] = patient_id
    message, checked = error_check(temppatient, value)
    if checked:
        hraverage = hr_averager(patient_id)
        return hraverage
    else:
        return message


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def interval_average():
    """Function that calculates average heart rate since an input time

    This function takes user input along with the patient ID number. The
    program then sends these values off to calculate the heart rate since the
    given input time.

    :return hraverage: The patient's average heart rate since the given time
    """
    value = 6
    # Gives average heart rate since the given time
    patienttime = request.get_json()

    uniqueid = patienttime["patient_id"]
    desiredtime = patienttime["heart_rate_average_since"]
    index = index_finder(uniqueid, desiredtime)
    hraverage = hr_averager(uniqueid, index)
    return hraverage


def error_check(patient, value):
    """The error checking function for the server

    This function performs a variety of error checking functions for the
    different methods on the server. It determines if the correct number of
    items in a list were given, whether the values are in the proper bounds,
    whether a given patient exists, etc.

    :param patient: The created patient whose data is being acted upon
    :param value: Which function is calling the errorchecker
    :return errormessage: The exact error that occurred
    :return error: A boolean indicating whether an error was deteced.
    """
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
    if value == 3 or value == 4 or value == 5:
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
            raise ValueError
    except ValueError:
        errormessage = jsonify("Patient " + str(uniqueid) +
                               " " + alreadypatient)
        error = False
    try:
        if str(uniqueid) not in masterlist and value > 1:
            raise ValueError
    except ValueError:
        errormessage = jsonify("Patient does not exist")
        error = False
    try:
        if "heart_rate" in keylist:
            if patient["heart_rate"] > 220 or patient["heart_rate"] < 10:
                raise ValueError
    except ValueError:
        error = False
        errormessage = jsonify("Heart Rate is out of bounds")

    return errormessage, error


def make_new_patient(patient):
    """Function that creates a new patient

    This function takes in a dictionary of information given by the user
    and then creates a patient with that information.

    :param patient: The input dictionary with patient information
    :return patient: Returns the patient that was created
    """
    uniqueid = patient["patient_id"]
    newtemppatient = Patient(patient_id=uniqueid,
                             attending_email=patient["attending_email"],
                             user_age=patient["user_age"],
                             hrlist=[],
                             timelist=[])
    # Hang onto this for if we get a database up and running
    # newtemppatient.save()
    masterlist[str(uniqueid)] = newtemppatient
    return patient


def set_heart_rate(hrset):
    """Function that sets a patient's heart rate

    This function takes a dictionary containing the patient's ID and
    their heart rate and then adds the given heart rate value to the
    list in the Patient object.

    :param hrset: Dictionary containing patient ID and heart rate value
    :return currenttime: Returns the time of the heart rate measurement.
    """
    uniqueid = hrset["patient_id"]
    temppatient = masterlist[str(uniqueid)]
    # Place the given heart rate in the heart rate list
    fullhrlist = temppatient.hrlist
    fulltimelist = temppatient.timelist
    temppatient.hrlist.append(hrset["heart_rate"])
    # Place the current time in the time list
    currenttime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    temppatient.timelist.append(currenttime)
    return currenttime


def getstatus(patient_id):
    """Function that checks the patient's tachycrdic status

    This function takes the patient's ID number and then checks based upon
    the patient's age and most recent heart rate information whether the
    patient is tachycardic or not.

    :param patient_id: The patient's ID number
    :return status: The patient's tachycardic status
    :return currenttime: The current time measured from the last HR recording.
    """

    temppatient = masterlist[patient_id]
    allhr = temppatient.hrlist
    alltime = temppatient.timelist
    age = int(temppatient.user_age)
    currenthr = allhr[-1]
    currenttime = alltime[-1]
    status, emailstatus = check_status(currenthr, age)

    return status, currenttime


def check_status(currenthr, age):
    """Fucntion that compares Age and HR to determine tachycardia

    This funciton uses a nest of if statements to determine whether
    the patient is tachycardic or not based upon their age.

    :param currenthr: The patient's current heart rate value
    :param age: The patient's age
    :return status: Whether the patient is tachycardic or not
    """
    emailsend = False
    status = "Not Tachycardic"
    if age == 1 or age == 2 and currenthr > 151:
        status = "Tachycardic"
        emailsend = True
    elif age == 3 or age == 4 and currenthr > 137:
        status = "Tachycardic"
        emailsend = True
    elif age >= 5 and age <= 7 and currenthr > 133:
        status = "Tachycardic"
        emailsend = True
    elif age >= 8 and age <= 11 and currenthr > 130:
        status = "Tachycardic"
        emailsend = True
    elif age >= 12 and age <= 15 and currenthr > 119:
        status = "Tachycardic"
        emailsend = True
    elif age > 15 and currenthr > 100:
        status = "Tachycardic"
        emailsend = True

    return status, emailsend


def get_hr(patient_id):
    """Function that returns the full hr list

    This function takes the patient's ID number and then returns their
    full list of HR measurements.

    :param patient_id: The patient's ID number
    :return fullhrlist: A list of the patient's heart rate values
    """
    temppatient = masterlist[str(patient_id)]
    fullhrlist = temppatient.hrlist
    return fullhrlist


def hr_averager(patient_id, index=0):
    """Function that averages all of a given patient's heart rate values

    :param patient_id: The patient's ID number
    :param index: The location at which to begin the averaging
    :return hravg: The average heart rate from the indicated point onwards
    """
    total = 0
    fullhrlist = get_hr(patient_id)
    hrlen = len(fullhrlist)
    print(hrlen)
    print(fullhrlist)
    for val in range(index, hrlen):
        total = fullhrlist[val] + total
        print(total)
    hravg = round(total/hrlen, 2)
    return str(hravg)


def index_finder(patient_id, time):
    """Function that determines the index for the averager to start on

    This function takes the patient's ID number and the input time and then
    computes the index for the heart rate average.

    :param patient_id: The patient's ID number
    :param time: The given time for comparison
    :return index: The index to start the averaging
    """
    index = 0
    temppatient = masterlist[str(patient_id)]
    fulltimelist = temppatient.timelist
    newtime = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    print(type(newtime))
    for x in fulltimelist:
        if newtime < x:
            break
        index += 1
    return index


if __name__ == "__main__":
    app.run(host="0.0.0.0")
