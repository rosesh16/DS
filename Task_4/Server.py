from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import time

class EHRServer:
    def __init__(self):
        self.doctors = {}
        self.patients = {}
        self.clients = {}  # client_id -> RPC address for clock sync

    # --- Doctor/Patient Management ---
    def add_doctor(self, did, details):
        self.doctors[did] = details
        return True

    def add_patient(self, pid, details):
        self.patients[pid] = details
        return True

    def get_patient(self, pid):
        return self.patients.get(pid)

    def update_patient(self, pid, updates):
        if pid not in self.patients:
            return None
        old_data = self.patients[pid].copy()
        self.patients[pid].update(updates)
        # Attach synchronized timestamp
        self.patients[pid]["last_updated"] = time.ctime(time.time())
        print(f"[SERVER] Patient {pid} updated: {self.patients[pid]}")
        return {"old": old_data, "new": self.patients[pid]}

    # --- Berkeley Clock Synchronization ---
    def register_client(self, cid, address):
        """Register client for clock sync"""
        self.clients[cid] = address
        return True

    def synchronize_clocks(self):
        local_time = time.time()
        offsets = []

        # Step 1: Poll all clients
        for cid, addr in self.clients.items():
            try:
                proxy = xmlrpc.client.ServerProxy(addr)
                client_time = proxy.get_local_time()
                offsets.append(client_time - local_time)
            except:
                pass  # ignore unreachable clients

        if not offsets:
            return "No clients to synchronize"

        # Step 2: Compute average offset
        avg_offset = sum(offsets) / len(offsets)

        # Step 3: Send adjustment to each client
        for cid, addr in self.clients.items():
            try:
                proxy = xmlrpc.client.ServerProxy(addr)
                proxy.adjust_clock(-avg_offset)
            except:
                pass

        return f"Clocks synchronized with avg offset {avg_offset:.3f} sec"

# --- Run Server ---
if __name__ == "__main__":
    server = SimpleXMLRPCServer(("localhost", 8000), logRequests=False,allow_none=True)
    server.register_instance(EHRServer())
    print("EHR Server running on port 8000...")
    server.serve_forever()
