# referenced https://medium.com/codex/tcp-vs-udp-a-deep-dive-into-server-client-communication-in-python-4339a973cabf
# for socket programming
# this link was provided in the course slide 2-165
from flask import Flask
from flask import request
import requests
import socket 

app = Flask(__name__)


@app.route("/fibonacci", methods = ["GET"])
def get_fibonacci():
    # get info from query string

    fs_port = request.args.get("fs_port")
    X = request.args.get("number")
    as_ip = request.args.get("as_ip")
    as_port = request.args.get("as_port")

    if fs_port is None or X is None or as_ip is None or as_port is None:
        return "Missing Parameters", 400

    # query DNS to get IP of Fibonacci server
    us_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    to_send = f"TYPE=A \nNAME=fibonacci.com"
    print("Sending DNS query")
    print(to_send)

    us_socket.sendto(to_send.encode(), (as_ip, int(as_port)))

    response, _ = us_socket.recvfrom(2048)
    print(response.decode())

    # extract IP of FS, hard code index because the DNS response has required format
    message = response.decode().replace("\n", "")
    fs_ip = message.split(" ")[2].split("=")[1]

    us_socket.close()
    print("Closed US socket")

    # server request fibonacci_server_ip/fibonacci?number=X
    res = requests.get(f"http://{fs_ip}:{int(fs_port)}/fibonacci?number={X}")

    # get response from FS
    # return answer
    if res.status_code == 200:
        return str(res.json()), 200
    else:
        return res.text, res.status_code



# delete later
app.run(host='0.0.0.0',port=8080,debug=False)