import xmlrpc.client
import time
from xmlrpc.server import SimpleXMLRPCServer
import threading

proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")
doctor_id = "D001"

# Register doctor
proxy.add_doctor(doctor_id, {"name": "Dr. Smith", "specialization": "Physician"})
proxy.register_client(doctor_id, "http://localhost:8001/")

# Local clock offset
clock_offset = 0.0

# --- Clock RPC Functions ---
def get_local_time():
    return time.time() + clock_offset

def adjust_clock(offset):
    global clock_offset
    clock_offset += offset
    return True

def clock_server():
    s = SimpleXMLRPCServer(("localhost", 8001), logRequests=False, allow_none=True)
    s.register_function(get_local_time, "get_local_time")
    s.register_function(adjust_clock, "adjust_clock")
    s.serve_forever()

# Start clock server in background
threading.Thread(target=clock_server, daemon=True).start()

# --- Doctor Operations ---
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
        print("\n--- Patient Record ---")
        for key, val in record.items():
            print(f"{key}: {val}")

        # Clock demo
        if "last_updated" in record:
            server_time = record["last_updated"]
            import time
            server_struct = time.strptime(server_time, "%a %b %d %H:%M:%S %Y")
            server_epoch = time.mktime(server_struct)
            local_view = time.ctime(server_epoch - (time.time() - (time.time() + clock_offset)))
            print(f"\n[Clock Comparison] Server: {server_time} | Doctor local view: {local_view}")
    else:
        print("Patient not found.")

def menu():
    while True:
        print("\n--- Doctor Menu ---")
        print("1. Add Patient")
        print("2. Update Patient")
        print("3. View Patient")
        print("4. Sync Clocks (Berkeley)")
        print("5. Exit")

        choice = input("Choose an option: ")
        if choice == "1":
            add_patient()
        elif choice == "2":
            update_patient()
        elif choice == "3":
            view_patient()
        elif choice == "4":
            msg = proxy.synchronize_clocks()
            print(f"⏱ {msg}")
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    menu()
