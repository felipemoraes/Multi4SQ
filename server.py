import os
import socket
import json
import sys
from collections import deque

HOST = '127.0.0.1'
PORT = 5005
BUFFER = 8192

# Startup server
clients = []
clientid = 0
server = socket.socket()
server.bind((HOST, PORT))
server.listen(socket.SOMAXCONN)

next_level = deque()
current_level = deque()
level_number = 0
size = int(sys.argv[1])
idlist = deque()
id_file = open('collected_ids', 'w')


while True:
    client, client_addr = server.accept()
    try:
        message = json.loads(client.recv(BUFFER))
        command = message["command"]
        print command,current_level
        if command == "GET_LOGIN":
            client_id = len(clients)
            clients.append(clientid)
            client.send(json.dumps({"command": "GIVE_LOGIN","clientid": client_id}))
        elif command == "GET_ID":
            #TODO: do a request to database getting venue and user id setting to correct status
            if current_level:
                ids = current_level.popleft()
                idlist.append(ids)
                client.send(json.dumps({"command" : "GIVE_ID", "idlist": ids, "level" : level_number}))
            elif size > level_number:
                for node_id in next_level:
                    current_level.append(node_id)
                next_level = deque()
                ids = current_level.popleft()
                idlist.append(ids)
                level_number += 1
                client.send(json.dumps({"command" : "GIVE_ID", "idlist": ids, "level" : level_number}))
            else:
                client.send(json.dumps({"command" : "FINISH"}))

        elif command == "UPDATE_ID":
            #TODO: update id in database
            ids = message["idlist"]
            id_file.write('%s;%d\n' % (ids,message['level']))
            client.send(json.dumps({"command" : "UPDATED_ID", "idlist": ids}))
            id_file.flush()
        elif command == "INSERT_ID":
            next_level.append(message['idlist'])


        elif command == "ERROR":
            #TODO: update id in database
            error_file.write('%s;%d\n' % (node_id,message['level']))
            client.send(json.dumps({"command" : "UPDATED_ID", "idlist": ids}))
    except Exception, e:
        print e
        pass
