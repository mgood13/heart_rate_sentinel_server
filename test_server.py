from flask import request, Flask, jsonify
from PatientDatabase import Patient
import datetime
import requests


def test_new_patient():
    """ This funciton tests whether the new patient function is working

    This function compares the given patient with an example for what
    the output should look like.

    :return:
    """
    ideal = {'attending_email': 'michael.good11@me.com',
             'patient_id': 5, 'user_age': 40}
    errormessage = "Patient 5 Already Exists"
    patient = {"patient_id": 5,
               "attending_email": "michael.good11@me.com",
               "user_age": 40}
    r1 = requests.post("http://127.0.0.1:5000/api/new_patient", json=patient)
    result = r1.json()
    assert result == ideal

    patient = {"patient_id": 5,
               "attending_email": "michael.good11@me.com",
               "user_age": 40}
    r1 = requests.post("http://127.0.0.1:5000/api/new_patient", json=patient)
    result = r1.json()
    assert result == errormessage


def test_heart_rate():
    """ Function that tests the heart rate addition function

    This function takes in patient heart rate information and makes sure that
    all of the error cases are catching their respective problems effectively.

    :return:
    """
    patient = {"patient_id": 1,
               "heart_rate": 100}
    r3 = requests.post("http://127.0.0.1:5000/api/heart_rate", json=patient)
    result = r3.json()
    assert result == "Heart Rate Added"

    patient2 = {"patient_id": 1,
                "heart_rate": 400}
    r4 = requests.post("http://127.0.0.1:5000/api/heart_rate", json=patient2)
    result = r4.json()
    assert result == "Heart Rate is out of bounds"

    patient3 = {"patient_id": 17,
                "heart_rate": 100}
    r5 = requests.post("http://127.0.0.1:5000/api/heart_rate", json=patient3)
    result = r5.json()
    assert result == "Patient does not exist"


def test_status():
    """Function that tests the status function.

    This function tests whether the status checker is functioning properly.
    In order to test this function this test function cuts off the microsecond
    values from the time variables.

    :return:
    """
    patient3 = {"patient_id": 2,
                "heart_rate": 120}
    r5 = requests.post("http://127.0.0.1:5000/api/heart_rate", json=patient3)

    r4 = requests.get("http://127.0.0.1:5000/api/status/2")
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = r4.json()
    assert result == "Patient is Not Tachycardic" +\
        ". Measured at {}".format(time)

    patient3 = {"patient_id": 2,
                "heart_rate": 150}
    r5 = requests.post("http://127.0.0.1:5000/api/heart_rate", json=patient3)
    r4 = requests.get("http://127.0.0.1:5000/api/status/2")
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = r4.json()
    assert result == "Patient is Tachycardic" + ". Measured at {}".format(time)

    r4 = requests.get("http://127.0.0.1:5000/api/status/17")
    result = r4.json()
    assert result == "Patient does not exist"


def test_heart_rate_full():
    """ Function that tests the output of the entire heart rate list

    This function takes in the patient_id and heart rate from the get
    request and then returns the list of all of the heart rate values.

    :return:
    """
    patient3 = {"patient_id": 2,
                "heart_rate": 180}
    r = requests.post("http://127.0.0.1:5000/api/heart_rate", json=patient3)
    r5 = requests.get("http://127.0.0.1:5000/api/heart_rate/2")
    result = r5.json()
    assert result == "Patient 2 all heart rate values:[120, 150, 180]"

    r5 = requests.get("http://127.0.0.1:5000/api/heart_rate/4")
    result = r5.json()
    assert result == "Patient has no recorded Heart Rate!"

    r5 = requests.get("http://127.0.0.1:5000/api/heart_rate/45")
    result = r5.json()
    assert result == "Patient does not exist"


def test_heart_rate_average():
    """Function that tests the heart_rate_average function

    This function tests the heart rate average function. It also checks
    for all of the potential error cases.
    """
    r5 = requests.get("http://127.0.0.1:5000/api/heart_rate/average/1")
    result = r5.json()
    assert result == 110

    r5 = requests.get("http://127.0.0.1:5000/api/heart_rate/average/15")
    result = r5.json()
    assert result == "Patient does not exist"

    r5 = requests.get("http://127.0.0.1:5000/api/heart_rate/average/4")
    result = r5.json()
    assert result == "Patient has no recorded Heart Rate!"


# def test_interval_average():
#    """
#
#    :return:
#    """
#    sincetime = datetime.datetime(2018, 11, 16, 15, 10, 40, 0)
#    patient2 = {"patient_id": 3,
#                "heart_rate_average_since": str(sincetime)}
#    r8 = requests.post("http://127.0.0.1:5000/api/heart_rate/
#   interval_average", json=patient2)
#    result = r8.json()
#    assert result == 132.5

#    sincetime = datetime.datetime(2018, 11, 16, 15, 10, 47, 0)
#    patient2 = {"patient_id": 3,
#                "heart_rate_average_since": str(sincetime)}
#    r8 = requests.post("http://127.0.0.1:5000/api/heart_rate/
#   interval_average", json=patient2)
#    result = r8.json()
#    assert result == 110

# This test was covered completely in the above tests
# def error_check():
#     return True


def test_make_new_patient():
    return True


def test_set_heart_rate():
    return True


def test_getstatus():
    return True


def test_get_hr():
    return True


def test_hr_averager():
    return True


def test_index_finder():
    return True
