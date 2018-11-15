import requests
def main():

    patient = {"patient_id": 3,
               "attending_email": "mgood10@jhu.edu",
               "user_age": 40}
    r2 = requests.post("http://127.0.0.1:5000/api/new_patient", json=patient)
    distance_result = r2.json()
    print(distance_result)

    patient2 = {"patient_id": 3,
                "heart_rate": 40}
    r3 = requests.post("http://127.0.0.1:5000/api/heart_rate", json=patient2)
    distance_result = r3.json()
    print(distance_result)



if __name__ == "__main__":
    main()
