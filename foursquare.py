import urllib2
import json
import gzip
import socket

HOST = ''
PORT = 5012
BUFFER = 8192
class FoursquareAPI:

    def request(self, url):
        #get access
        access = socket.socket()
        access.connect((HOST, PORT))
        access.send(json.dumps({"command" : "GET_ACCESS"}))
        message = json.loads(access.recv(BUFFER))
        access_token = message['key']
        url += "&oauth_token=%s&v=20140526" % access_token
        print url
        data = urllib2.urlopen(url)
        result = json.load(data)
        return result

    def user_basic_info(self, user_id):
        url = "https://api.foursquare.com/v2/users/%s?" % (user_id)
        response = self.request(url)
        self.save(response,'4sq_user_basic_info_%s.json.gzip' % user_id)

    def user_friendship(self, user_id):
        friends = []
        url = "https://api.foursquare.com/v2/users/%s/friends?limit=500" % (user_id)
        response = self.request(url)
        for friend in response['response']['friends']['items']:
            friends.append(friend['id'])
        count = response['response']['friends']['count']
        self.save(response,'4sq_user_friends_%s.json.gzip' % (user_id))
        count -= len(response['response']['friends']['items'])
        offset = len(response['response']['friends']['items'])
        while count:
            url = "https://api.foursquare.com/v2/users/%s/friends?limit=500&offset=%s" % (user_id, offset)
            response = self.request(url)
            for friend in response['response']['friends']['items']:
                friends.append(friend['id'])
            self.save(response,'4sq_user_friends_%s_%d.json.gzip' % (user_id,offset))
            count -= len(response['response']['friends']['items'])
            offset += len(response['response']['friends']['items'])
        return friends

    def user_tips(self, user_id):
        url = "https://api.foursquare.com/v2/lists/%s/tips?limit=500" % (user_id)
        response = self.request(url)
        count = response['response']['list']['listItems']['count']
        count -= len(response['response']['list']['listItems']['items'])
        self.save(response,'4sq_user_tips_%s.json.gzip' % (user_id))
        offset = len(response['response']['list']['listItems']['items'])
        while count:
            if not(len(response['response']['list']['listItems']['items'])):
                break
            url = "https://api.foursquare.com/v2/lists/%s/tips?limit=500&offset=%s" % (user_id, offset)
            response = self.request(url)
            self.save(response,'4sq_user_tips_%s_%d.json.gzip' % (user_id,offset))
            count -= len(response['response']['list']['listItems']['items'])
            offset += len(response['response']['list']['listItems']['items'])

    def user_venueslikes(self, user_id):
        url = "https://api.foursquare.com/v2/users/%s/venuelikes?limit=500" % (user_id)
        response = self.request(url)
        count = response['response']['venues']['count']
        count -= len(response['response']['venues']['items'])
        self.save(response,'4sq_user_venueslikes_%s.json.gzip' % (user_id))
        offset = len(response['response']['venues']['items'])
        while count:
            if not(len(response['response']['venues']['items'])):
                break
            url = "https://api.foursquare.com/v2/users/%s/venuelikes?limit=500&offset=%s" % (user_id, offset)
            response = self.request(url)
            self.save(response,'4sq_user_venueslikes_%s_%d.json.gzip' % (user_id,offset))
            count -= len(response['response']['venues']['items'])
            offset += len(response['response']['venues']['items'])

    def user_mayorships(self, user_id):
        url = "https://api.foursquare.com/v2/users/%s/mayorships?" % (user_id)
        response = self.request(url)
        self.save(response, '4sq_user_mayorship_%s.json.gzip' % user_id)

    def user_badges(self, user_id):
        url = "https://api.foursquare.com/v2/users/%s/badges?" % (user_id)
        response = self.request(url)
        self.save(response, '4sq_user_badges_%s.json.gzip' % user_id)

    def venue_basic_info(self, venue_id):
        url = "https://api.foursquare.com/v2/venues/%s?" % (venue_id)
        response = self.request(url)
        self.save(response,'4sq_venue_basic_info_%s.json.gzip' % venue_id)
    def venue_likes(self, venue_id):
        url = "https://api.foursquare.com/v2/venues/%s/likes" (venue_id)
        response = self.request(url)
        self.save(response,'4sq_venue_likes_%s.json.gzip' % venue_id)

    def venue_tips(self, venue_id):
        url = "https://api.foursquare.com/v2/venues/%s/tips?limit=500" % (venue_id)
        response = self.request(url)
        count = response['response']['tips']['count']
        self.save(responses,'4sq_venue_tips_%s.json.gzip' % (venue_id))
        count -= len(response['response']['tips']['items'])
        offset = len(response['response']['tips']['items'])
        while count:
            url = "https://api.foursquare.com/v2/venues/%s/tips?limit=500&offset=%s" % (venue_id, offset)
            response = self.request(url)
            self.save(responses,'4sq_venue_tips_%s_%d.json.gzip' % (venue_id,offset))
            count -= len(response['response']['tips']['items'])
            offset += len(response['response']['tips']['items'])

    def tips_basic_info(self, tip_id):
        url = "https://api.foursquare.com/v2/tips/%s?oauth_token=%s&v=20140526" (tip_id)
        response = self.request(url)
        self.save(response,'4sq_tip_basic_info_%s.json.gzip' % venue_id)

    def tips_likes(self, tip_id):
        url = "https://api.foursquare.com/v2/tips/%s/likes?oauth_token=%s&v=20140526" (tip_id, self.access_token)
        response = self.request(url)
        self.save(response,'4sq_tip_likes_%s.json.gzip' % venue_id)
    def save(self, response, filename):
        fout = gzip.open('data/' + filename,'w')
        fout.write(json.dumps(response))




#access_token = "RTZE0LDMEDZ4HJ01CJ1NW3YODCLUP1GC1XYMSC41B1NY2R1D"
#api = FoursquareAPI()
#user_id = '525730'
#print api.user_friendship(user_id)
#api.user_basic_info(user_id)
#api.user_tips(user_id)
#api.user_venueslikes(user_id)


