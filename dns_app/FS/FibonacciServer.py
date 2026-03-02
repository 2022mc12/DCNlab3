# referenced https://medium.com/codex/tcp-vs-udp-a-deep-dive-into-server-client-communication-in-python-4339a973cabf
# for socket programming
# this link was provided in the course slide 2-165

from flask import Flask
from flask import request
import socket
app = Flask(__name__)



# handle PUT request
# parse the input and register with AS
# send back 200 
@app.route("/register", methods = ["PUT"])
def register():
    register_data = request.get_json()
    print(register_data)

    print("started registration")
    fs_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    to_send = f"TYPE=A \nNAME={register_data['hostname']} VALUE={register_data['ip']} TTL=10"
    fs_socket.sendto(to_send.encode(), (register_data['as_ip'], int(register_data['as_port'])))
    response, _ = fs_socket.recvfrom(2048)
    print(response.decode())

    fs_socket.close()
    print("Closed FS socket")

    return "Registration Successful", 201


# handle GET request 
@app.route("/fibonacci", methods = ["GET"])
def fibonacci():
    X = request.args.get("number")

    try:
        X = int(X)
    except: 
        return "Bad Format: X needs to be an integer", 400
    
    
    x1 = 0
    x2 = 1 

    if X == 1: return str(x1), 200 
    if X ==2: return str(x2), 200

    for i in range(X-2):
        temp = x1+x2
        x1 = x2
        x2 = temp 
    
    return str(x2), 200
   




# delete later
app.run(host='0.0.0.0',
        port=9090,
        debug=False)