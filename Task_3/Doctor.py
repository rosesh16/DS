import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

# Register the doctor (you can expand later for multiple doctors)
doctor_id = "D001"
proxy.add_doctor(doctor_id, {"name": "Dr. Smith", "specialization": "Physician"})

def add_patient():
    pid = input("Enter Patient ID: ")
    name = input("Enter Patient Name: ")
    age = int(input("Enter Patient Age: "))
    diagnosis = input("Enter Patient Diagnosis: ")
    prescription = input("Enter Patient Prescription: ")
    details = {"name": name, "age": age, "diagnosis": diagnosis, "prescription": prescription}
    proxy.add_patient(pid, details)
    print(f"Patient {pid} added.")

def update_patient():
    pid = input("Enter Patient ID to update: ")
    record = proxy.get_patient(pid)
    if not record:
        print("Patient not found.")
        return

    print("Current details:", record)
    diagnosis = input("Enter new Diagnosis: ")
    prescription = input("Enter new Prescription: ")
    update_info = proxy.update_patient(pid, {"diagnosis": diagnosis, "prescription": prescription})

    if update_info:
        print("Patient updated successfully. Changes:")
        for key in update_info["new"]:
            old_val = update_info["old"].get(key)
            new_val = update_info["new"].get(key)
            if old_val != new_val:
                print(f"  - {key}: {old_val} ➝ {new_val}")
    else:
        print("Update failed.")

def view_patient():
    pid = input("Enter Patient ID to view: ")
    record = proxy.get_patient(pid)
    if record:
        print("Patient Record:", record)
    else:
        print("Patient not found.")

def menu():
    while True:
        print("\n--- Doctor Menu ---")
        print("1. Add Patient")
        print("2. Update Patient")
        print("3. View Patient")
        print("4. Exit")

        choice = input("Choose an option: ")
        if choice == "1":
            add_patient()
        elif choice == "2":
            update_patient()
        elif choice == "3":
            view_patient()
        elif choice == "4":
            print("Exiting Doctor Client...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    menu()
