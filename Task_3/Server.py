from xmlrpc.server import SimpleXMLRPCServer

class EHRServer:
    def __init__(self):
        self.patients = {}
        self.doctors = {}

    # Patient methods
    def add_patient(self, patient_id, details):
        self.patients[patient_id] = details
        return True

    def update_patient(self, patient_id, details):
        if patient_id in self.patients:
            old_details = self.patients[patient_id].copy()
            self.patients[patient_id].update(details)
            print(f"[SERVER] Patient {patient_id} updated: {self.patients[patient_id]}")
            return {"old": old_details, "new": self.patients[patient_id]}
        return None

    def get_patient(self, patient_id):
        return self.patients.get(patient_id, None)

    # Doctor methods
    def add_doctor(self, doctor_id, details):
        self.doctors[doctor_id] = details
        return True

    def update_doctor(self, doctor_id, details):
        if doctor_id in self.doctors:
            self.doctors[doctor_id].update(details)
            return True
        return None

    def get_doctor(self, doctor_id):
        return self.doctors.get(doctor_id, None)


if __name__ == "__main__":
    server = SimpleXMLRPCServer(("localhost", 8000))
    ehr = EHRServer()
    server.register_instance(ehr)
    print(" EHR Server running on port 8000...")
    server.serve_forever()
