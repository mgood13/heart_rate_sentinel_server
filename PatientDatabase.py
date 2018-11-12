from pymodm import connect
from pymodm import MongoModel, fields


connect("mongodb://mjg56:DukeBME13@ds159563.mlab.com:59563/bme590hrserver")

class Patient(MongoModel):
    patient_id = fields.CharField(primary_key=True)
    attending_email = fields.EmailField()
    user_age = fields.CharField()
