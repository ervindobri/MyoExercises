import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from constants.variables import RESOURCES_PATH


class FirestoreDatabase:
    def __init__(self):
        cred = credentials.Certificate(RESOURCES_PATH + "myoexercises-firebase-adminsdk-gx5fr-5b5c17c132.json")
        firebase_admin.initialize_app(cred, {
            'projectId': 'myoexercises',
        })

        db = firestore.client()

        self.patients = db.collection(u'patients')
        self.session = db.collection(u'session')

    def set_session_data(self, reps, rest):
        data = {
            u'reps': reps,
            u'rest': rest
        }
        self.session.document('main').set(data)

    def set_patient_data(self, patient):
        print("Patient:", patient.name)
        data = {
            u'name': patient.name,
            u'age': patient.age,
            u'exercises': patient.exercises
        }
        self.patients.document(patient.name + '-' + str(patient.age)).set(data)