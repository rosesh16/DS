import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")
pid = input("Enter your Patient ID: ")

record = proxy.get_patient(pid)
if record:
    print("Your Record:", record)
else:
    print("No record found.")
