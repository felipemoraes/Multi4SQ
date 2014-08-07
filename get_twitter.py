from twitter import *
import gzip
import json
import time
import re

for line in open('collected_ids'):
  line = re.split(';',line)
  user_id = line[0]
  fin = gzip.open('data/4sq_user_basic_info_%s.json.gzip' % user_id)
  content = json.load(fin)
  if content['response']['user']['contact'].has_key('twitter'):
    twitter_id = content['response']['user']['contact']['twitter']
    api = getTwitterUser(twitter_id)
    followers = api.followers()
    following = api.following()
    print twitter_id
    fout = gzip.open('data/4sq_user_twitter_%s.json.gzip' % user_id, 'w')
    fout.write(json.dumps({'followers': followers, 'following': following}))
    fout.close()
    time.sleep(60)
