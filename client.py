import os
import socket
import json
from foursquare import FoursquareAPI
import threading


HOST = 'localhost'
PORT = 5005
BUFFER = 8192
process_id = os.getpid()
server = socket.socket()
server.connect((HOST, PORT))
server.send(json.dumps({"command": "GET_LOGIN", "processid": process_id, "clientid": 0}))
message = json.loads(server.recv(BUFFER))
server.close()
client_id = message["clientid"]
N_THREAD = 1

class Thread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name,verbose=verbose)
        self.args = args
        return

    def run(self):
        while True:
            global HOST, PORT
            server = socket.socket()
            server.connect((HOST,PORT))
            print "get id"
            server.send(json.dumps({"command": "GET_ID","clientid":client_id}))
            message = json.loads(server.recv(BUFFER))
            server.close()
            print "get id"
            command = message["command"]
            print command
            if command == "GIVE_ID":
                ids = message["idlist"]
                level = message["level"]
                try:
                	self.collect_ids(ids)
                	server = socket.socket()
                	server.connect((HOST,PORT))
                	server.send(json.dumps({"command": "UPDATE_ID","clientid":client_id, "idlist":ids, "level": level}))
                   	message = json.loads(server.recv(BUFFER))
                   	server.close()

                except Exception, e:
                    server = socket.socket()
                    server.connect((HOST,PORT))
                    server.send(json.dumps({"command": "ERROR","clientid":client_id, "idlist":ids, "level": level}))
                    message = json.loads(server.recv(BUFFER))
                    server.close()


            elif command == "FINISH":
                return


    def collect_ids(self, ids):
    	api = FoursquareAPI()
        api.user_basic_info(ids)
        api.user_tips(ids)
        api.user_venueslikes(ids)
        listids = api.user_friendship(ids)
        for user_id in listids:
            server = socket.socket()
            server.connect((HOST,PORT))
            server.send(json.dumps({"command": "INSERT_ID","clientid":client_id, "idlist":user_id}))
            server.close()




try:
    threads=[]
    for i in xrange(N_THREAD):
        t = Thread(args=(client_id,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

except Exception, e:
    print "ERROR", e
