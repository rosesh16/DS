import xmlrpc.client
import time
from xmlrpc.server import SimpleXMLRPCServer
import threading

proxy = xmlrpc.client.ServerProxy("http://localhost:8000/",allow_none=True)
patient_id = "P001"

# Register patient
proxy.register_client(patient_id, "http://localhost:8002/")

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
    s = SimpleXMLRPCServer(("localhost", 8002), logRequests=False, allow_none=True)
    s.register_function(get_local_time, "get_local_time")
    s.register_function(adjust_clock, "adjust_clock")
    s.serve_forever()

threading.Thread(target=clock_server, daemon=True).start()

# --- Patient Operations ---
def view_patient():
    pid = input("Enter your Patient ID: ")
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
            print(f"\n[Clock Comparison] Server: {server_time} | Patient local view: {local_view}")
    else:
        print("No record found.")

def menu():
    while True:
        print("\n--- Patient Menu ---")
        print("1. View My Record")
        print("2. Synchronize Clocks (Berkeley)")
        print("3. Exit")

        choice = input("Choose an option: ")
        if choice == "1":
            view_patient()
        elif choice == "2":
            msg = proxy.synchronize_clocks()
            print(f"⏱ {msg}")
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    menu()
