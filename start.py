import json
import tweepy
import logging
import urllib2
import re
import time
from urlunshort import resolve
from geopy.distance import great_circle
import os
import socket
from foursquare import FoursquareAPI

#Logging
logging.basicConfig(format='[%(asctime)s] %(levelname)s:  %(message)s', datefmt='%d/%m/%Y %H:%M:%S', filename='log/errors.log', filemode='a', level=logging.INFO)
tweets = open('tweet_ids', 'a')
#Keys

consumer_key = "<Your Consumer Key>"
consumer_secret = "Your Consumer Secret"
access_token = "Your Access Token"
access_token_secret = "Your Access Token Secret"


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

class StdOutListener(tweepy.streaming.StreamListener):

    counter = 0

    def __init__(self, cnt):
        self.counter = cnt

    def on_data(self, data):
        try:
            data_obj = json.loads(data)
            if "id" not in data_obj:
                logging.error("ID not found. Json = %s" % data_obj)
                return True
            coordinates = data_obj["coordinates"]["coordinates"]
            distance = great_circle((coordinates[1],coordinates[0]), (40.7127, -74.0059)).km
            if distance < 1500:
                tweet_id = data_obj["id"]
                tweets.write("%s\n" % tweet_id)
                print "Colect. %d" % self.counter

                url = data_obj["entities"]["urls"][0]["expanded_url"]
                self.process_url(url)
                self.counter += 1
                exit()
            return True

        except Exception, e:
            self.counter = self.counter + 1
            logging.error("Unknown Error: %s" % str(e))
    def on_error(self, status):
        logging.error("Streaming error: %s" % str(status))
        return True

    def process_url(self, url):
        expanded_url = resolve(url)
        response = urllib2.urlopen(url)
        page = response.read()
        user_id = re.findall("\"id\":\"[0-9]+\"", page)
        user_id = "{" + user_id[0] + "}"
        user_id = json.loads(user_id)
        user_id = user_id["id"]
        print user_id
        api = FoursquareAPI()
        listids = api.user_friendship(user_id)
        api.user_tips(user_id)
        api.user_venueslikes(user_id)
        server = socket.socket()
        server.connect((HOST,PORT))
        server.send(json.dumps({"command": "UPDATE_ID","clientid":client_id, "idlist":user_id, "level": 0}))
        message = json.loads(server.recv(BUFFER))
        server.close()
        print listids
        api.user_basic_info(user_id)
        for user_id in listids:
            server = socket.socket()
            server.connect((HOST,PORT))
            server.send(json.dumps({"command": "INSERT_ID","clientid":client_id, "idlist":user_id}))
            server.close()

def main():
    logging.info("Starting crawler")

    terms = ["4sq"]
    logging.info("+ Loading {} terms".format(len(terms)))

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    logging.info("Authentication on twitter")
    # Setting geolocations
    geoterms =[-74.550691,40.424997,-73.295717,41.178654]
    # Setting Streaming for monitor terms
    listener = StdOutListener(0)
    stream = tweepy.Stream(auth, listener)
    logging.info("Starting streaming")
    stream.filter(track=terms)
    stream.filter(locations = geoterms)



if __name__ == "__main__":
    main()

