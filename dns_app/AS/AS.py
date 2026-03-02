# referenced https://medium.com/codex/tcp-vs-udp-a-deep-dive-into-server-client-communication-in-python-4339a973cabf
# this link was provided in the course slide 2-165

import socket 

# use a list to keep track of servers and addresses
# each entry is (Name, Value, Type, TTL)
DNS = []


as_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

port = 53533

as_socket.bind(('0.0.0.0', port))
print("Listening")

while True: 
    message, client_address = as_socket.recvfrom(2048)


    # take out new line so its easier to parse 
    message = message.decode().replace("\n", "")
    message_parts = message.split(" ")

    if len(message_parts) == 2:
        # this is a DNS query 
        # hard coded indicies because the input is always in this format
        name = message_parts[1].split("=")[1] # gets the name 
        print(f"Querying")

        for (entry_name, entry_val, entry_type, entry_ttl) in DNS:
            if entry_name == name:
                to_send = f"TYPE={entry_type} \nNAME={entry_name} VALUE={entry_val} TTL={entry_ttl}"
                print(to_send)
                as_socket.sendto(to_send.encode(), client_address)
    elif len(message_parts) == 4: 
        # this is a Registration
        print("Registering")
        all_vals = [] # will be in [Type, Name, Value, TTL] format
        for part in message_parts:
            key, val = part.split("=")
            all_vals.append(val)

        # rearrange the values to enter into DNS
        # format: (Name, Value, Type, TTL)
        # hard coded indicies because the input is always in this format
        entry = (all_vals[1], all_vals[2], all_vals[0], all_vals[3])
        DNS.append(entry)
        print(entry)
        as_socket.sendto("success".encode(),client_address)
    else:
        as_socket.sendto("error".encode(),client_address)





as_socket.close()
