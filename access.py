import sys
import socket
import json
import datetime
from collections import deque
import time

PORT = 5012
BUFFER = 8192


# Startup server
clients = []
server = socket.socket()
server.bind(("", PORT))
server.listen(socket.SOMAXCONN)

fin = open("access_keys","r")
keys = {}
for line in fin:
    key = line.strip("\n")
    keys[key] = {"count":0, "time": time.time()}
print keys
while True:
    client,client_addr = server.accept()
    print keys
    message_text = client.recv(BUFFER)
    try:
        message = json.loads(message_text)
        command = message["command"]
        aux = True
        while aux:
            for key in keys:
                if keys[key]["count"] < 500:
                    client.send(json.dumps({"command": "GIVE_ACCESS", "key": key}))
                    keys[key]["count"] += 1
                    aux = False
                    break
                elif (time.time() - keys[key]["time"]) >= 3600:
                    keys[key]["count"] = 1
                    client.send(json.dumps({"command": "GIVE_ACCESS", "key": key}))
                    keys[key]["time"] = time.time()
                    aux = False
                    print "Is back!"
                    break


    except Exception, error:
        print "Client ERROR: %s" % (str(error))
        client.send(json.dumps({"command": "FINISH"}))
        client.close()
        break

    print "fechou conexao"
    client.close()
