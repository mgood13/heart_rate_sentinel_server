import requests
def main():

    patient = {"patient_id": 1,
               "attending_email": mgood10@jhu.edu,
               "user_age": 30}
    r2 = requests.post("http://127.0.0.1:5000/api/new_patient", json=patient)
    distance_result = r2.json()
    print(distance_result)
    #print("The total is {0}.".format(sum_result['result']))


if __name__ == "__main__":
    main()
