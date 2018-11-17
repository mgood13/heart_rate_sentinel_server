import requests
import datetime


def main():
    """This function prepares the server with test cases

    Running this function will add example patients to the dictionary on the
    server which are later used for the functionality testing.

    :return:
    """
    patient1 = {"patient_id": 1,
                "attending_email": "michael.good11@me.com",
                "user_age": 5}
    patient2 = {"patient_id": 2,
                "attending_email": "michael.good11@me.com",
                "user_age": 7}
    patient3 = {"patient_id": 3,
                "attending_email": "michael.good11@me.com",
                "user_age": 100}
    patient4 = {"patient_id": 4,
                "attending_email": "michael.good11@me.com",
                "user_age": 30}
    requests.post("http://vcm-7453.vm.duke.edu:5000/api/new_patient", json=patient1)
    requests.post("http://vcm-7453.vm.duke.edu:5000/api/new_patient", json=patient2)
    requests.post("http://vcm-7453.vm.duke.edu:5000/api/new_patient", json=patient3)
    requests.post("http://vcm-7453.vm.duke.edu:5000/api/new_patient", json=patient4)

    patient3 = {"patient_id": 1,
                "heart_rate": 120}
    requests.post("http://vcm-7453.vm.duke.edu:5000/api/heart_rate", json=patient3)

    patient200 = {"patient_id": 200,
                  "attending_email": "michael.good11@me.com",
                  "user_age": 30,
                  "hrlist": [200, 100, 120, 110],
                  "timelist":
                      [datetime.datetime(2018, 11, 16, 15, 10, 45, 469586),
                             datetime.datetime(2018, 11, 16, 15, 10,
                                               50, 669845),
                             datetime.datetime(2018, 11, 16, 15, 10,
                                               50, 725354),
                             datetime.datetime(2018, 11, 16, 15, 10,
                                               50, 834356)]}
    requests.post("http://vcm-7453.vm.duke.edu:5000/api/new_patient", json=patient1)


if __name__ == "__main__":
    main()
