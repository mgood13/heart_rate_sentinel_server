import requests
import datetime
def main():

    patient = {"patient_id": 3,
               "attending_email": "mgood10@jhu.edu",
               "user_age": 40}
    r2 = requests.post("http://127.0.0.1:5000/api/new_patient", json=patient)
    distance_result = r2.json()
    print(distance_result)

    patient2 = {"patient_id": 3,
                "heart_rate": 100}
    r3 = requests.post("http://127.0.0.1:5000/api/heart_rate", json=patient2)
    distance_result = r3.json()
    print(distance_result)
    patient2 = {"patient_id": 3,
                "heart_rate": 100}
    r3 = requests.post("http://127.0.0.1:5000/api/heart_rate", json=patient2)
    distance_result = r3.json()
    print(distance_result)
    patient2 = {"patient_id": 3,
                "heart_rate": 100}
    r3 = requests.post("http://127.0.0.1:5000/api/heart_rate", json=patient2)
    distance_result = r3.json()
    print(distance_result)

    r7 = requests.get("http://127.0.0.1:5000/api/heart_rate/average/3")
    avg = r7.json()
    print(avg)


    #r4 = requests.get("http://127.0.0.1:5000/api/status/3")
    #distance_result = r4.json()
    #print(distance_result)

    #r6 = requests.get("http://127.0.0.1:5000/api/heart_rate/3")
    #message = r5.json()
    #result = r6.json()
    #print(result)
    #print(message)
    sincetime = datetime.datetime(2018, 11, 15, 18, 16, 40, 0)
    patient2 = {"patient_id": 3,
                "heart_rate_average_since": str(sincetime)}
    r8 = requests.post("http://127.0.0.1:5000/api/heart_rate/interval_average", json=patient2)
    distance_result = r3.json()
    print(distance_result)



if __name__ == "__main__":
    main()
