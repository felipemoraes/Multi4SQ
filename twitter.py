from TwitterAPI import TwitterAPI
import time
import sys 

class getTwitterUser:

   consumer_key = None
   consumer_secret = None
   access_token_key = None
   access_token_secret = None
   api = None
   user_id = None

   def __init__(self,user):
       #TODO
      self.consumer_key = "Your Consumer Key"
      self.consumer_secret = "Your Consumer Secret"
      self.access_token_key = "Your Access Token Key"
      self.access_token_secret = "Your Access Token Secret"
      self.api = TwitterAPI(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret)
      self.user_id = self.get_user_id(user)
      
   def basic_info(self): 
      res = self.api.request('users/show', {'user_id': self.user_id})
      iter = res.get_iterator()
      itens = []
      for item in iter:
         itens.append(item)
      return itens

   def get_user_id(self, username):
      res = self.api.request('users/lookup', {'screen_name': username})
      iter = res.get_iterator()
      items = []
      for item in iter:
         items.append(item)
      if items[0].has_key('id'):
          return items[0]['id']
      else:
          return None

   def following(self):
      res = self.api.request('friends/ids',{'user_id': self.user_id})
      iter = res.get_iterator()
      itens = []
      itens_all = []
      for item in iter:
         itens.append(item)
         itens_all.append(item)
      try:
         cursor = itens[0]['next_cursor']
      except:
         return itens_all
      while True:
         if cursor:
            itens = []
            time.sleep(60)
            res = self.api.request('friends/ids',{'user_id': self.user_id, 'cursor': cursor, 'count': 5000})
            iter = res.get_iterator()
            for item in iter:
               itens.append(item)
               itens_all.append(item)
            cursor = itens[0]['next_cursor']
         else:
            break   
      return itens_all

   def followers(self):
      res = self.api.request('followers/ids',{'user_id': self.user_id})
      iter = res.get_iterator()
      itens = []
      itens_all = []
      for item in iter:
         itens.append(item)
         itens_all.append(item)
      try:
         cursor = itens[0]['next_cursor']
      except:
         return itens_all
      while True:
         if cursor:
            itens = []
            time.sleep(60)
            res = self.api.request('followers/ids',{'user_id': self.user_id, 'cursor': cursor, 'count': 5000})
            iter = res.get_iterator()
            for item in iter:
               itens.append(item)
               itens_all.append(item)
            cursor = itens[0]['next_cursor']
         else:
            break   
      return itens_all

   def tweets(self):
      res = self.api.request('statuses/user_timeline',{'user_id': self.user_id, 'count':200})
      iter = res.get_iterator()
      tweets = []
      tweets_all = []
      for item in iter:
         tweets.append(item)
         tweets_all.append(item)
      length = len(tweets_all)
      max_id = tweets[0]['id']
      while len(tweets) == 200:
         res = self.api.request('statuses/user_timeline',{'user_id': self.user_id, 'count':200, 'max_id':max_id})
         iter = res.get_iterator()
         tweets = []
         for item in iter:
            tweets.append(item)
            tweets_all.append(item)
         length = len(tweets_all)
         max_id = tweets[0]['id']
         return tweets_all


