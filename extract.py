import gzip
import json
import glob
import re
import sys
import networkx as nx


def load_hops(sb_size):
   hops = {}
   for line in open('collected_ids'):
      line = line.strip('\n')
      line = re.split(';', line)
      user = line[0]
      hop = int(line[1])
      if hop <= sb_size:
         if hops.has_key(hop):
            hops[hop].append(user)
         else:
            hops[hop] = [user]
   return hops


def load_users_tips(users_hops,graph):
   users_tips = {}
   users = []
   for hop_list in users:
      users += hop_list
   for user_id in users:
      fin = gzip.open('data/4sq_user_tips_%s.json.gzip' % user_id)
      response = json.load(fin)
      offset = len(response['response']['list']['listItems']['items'])
      count = response['response']['list']['listItems']['count']
      count -= len(response['response']['list']['listItems']['items'])
      users_tips[user_id] = []
      for item in response['response']['list']['listItems']['items']:
         users_tips[user_id].append([item['venue']['id'],item['createdAt']])
      if count:
         for fname in glob.glob('data/4sq_user_tips_%s_*.json.gzip' % user_id):
            fin = gzip.open(fname)
            response = json.load(fin)
            for item in response['response']['list']['listItems']['items']:
               users_tips[user_id].append([item['venue']['id'],item['createdAt']])

   for user1 in users:
      for user2 in users:
         if user1 == user2:
             continue
         for venue1 in users_tips[user1]:
            for venue2 in users_tips[user2]:
               if venue1[0] == venue2[0]:
                  if graph.has_edge(user, friend):
                     if 'tips' not in graph[user][friend]['labels']:
                        graph[user][friend]['labels'].append('tips')
                  else:
                     graph.add_edge(user,friend)
                     graph[user][friend]['labels'] = ['tips']
   return graph
def load_users_venues(users_hops, graph):
   users_venues = {}
   users = []
   for hop_list in users_hops.values():
      users += hop_list
   for user_id in users:
      fin = gzip.open('data/4sq_user_venueslikes_%s.json.gzip' % user_id)
      response = json.load(fin)
      offset = len(response['response']['venues']['items'])
      count = response['response']['venues']['count']
      count -= len(response['response']['venues']['items'])
      users_venues[user_id] = []
      for item in response['response']['venues']['items']:
         users_venues[user_id].append(item['id'])
      if count:
         for fname in glob.glob('data/4sq_user_venueslikes_%s_*.json.gzip' % user_id):
            fin = gzip.open(fname)
            response = json.load(fin)
            for item in response['response']['venues']['items']:
               users_venues[user_id].append(item['id'])

   for user1 in users:
      for user2 in users:
         if user1 == user2:
             continue
         for venue1 in users_venues[user1]:
            for venue2 in users_venues[user2]:
               if venue1 == venue2:
                  if graph.has_edge(user1, user2):
                     if 'venueslikes' not in graph[user1][user2]['labels']:
                        graph[user1][user2]['labels'].append('venueslikes')
                  else:
                     graph.add_edge(user1,user2)
                     graph[user1][user2]['labels'] = ['venueslikes']
      return graph

def load_users_friends(users_hops,sb_size):
   graph = nx.Graph()
   users_friends = {}
   users = []
   for hop_list in users_hops.values():
      users += hop_list
   for user_id in users:
      fin = gzip.open('data/4sq_user_friends_%s.json.gzip' % user_id)
      response = json.load(fin)
      offset = len(response['response']['friends']['items'])
      count = response['response']['friends']['count']
      users_friends[user_id] = []
      if user_id in users_hops[sb_size]:
         for item in response['response']['friends']['items']:
            if item['id'] in users_hops.values():
               users_friends[user_id].append(item['id'])
         if count:
            for fname in glob.glob('data/4sq_user_venueslikes_%s_*.json.gzip' % user_id):
               fin = gzip.open(fname)
               response = json.load(fin)
               for item in response['response']['venues']['items']:
                  if item['id'] in users_hops.values():
                     users_friends[user_id].append(item['id'])
      else:
         for item in response['response']['friends']['items']:
            users_friends[user_id].append(item['id'])
            if count:
               for fname in glob.glob('data/4sq_user_venueslikes_%s_*.json.gzip' % user_id):
                  fin = gzip.open(fname)
                  response = json.load(fin)
                  for item in response['response']['venues']['items']:
                     users_friends[user_id].append(item['id'])
   for user in users_friends:
      for friend in users_friends[user]:
         if graph.has_edge(user, friend):
            if 'friend' not in graph[user][friend]['labels']:
               graph[user][friend]['labels'].append('friend')
         else:
            graph.add_edge(user,friend)
            graph[user][friend]['labels'] = ['friend']
   return graph


def load_twitter(users_hops,graph):
   twitter_ids = {}
   users = []
   for hop_list in users_hops.values():
      users += hop_list
   for user_id in users:
      try:
         fout = gzip.open('4sq_user_twitter_%s.json.gzip' % user_id, 'r')
         content = json.load(fout)
      except:
         continue
      twitter_ids[content['twitter_id']] = user_id

   for user_id in users:
      try:
         fout = gzip.open('4sq_user_twitter_%s.json.gzip' % user_id, 'r')
         content = json.load(fout)
      except:
         continue
      for page in content['followers']:
         if not page.has_key('ids'):
           continue
         for twitter_id in page['ids']:
            if twitter_id in twitter_ids.keys():
               user2 = twitter_ids[twitter_id]
               if graph.has_edge(user_id, user2):
                  if 'twitter' not in graph[user_id][user2]['labels']:
                     graph[user_id][user2]['labels'].append('twitter')
               else:
                  graph.add_edge(user,friend)
                  graph[user_id][user2]['labels'] = ['twitter']

      for page in content['following']:
         if not page.has_key('ids'):
            continue
         for twitter_id in page['ids']:
            if twitter_id in twitter_ids.keys():
               user2 = twitter_ids[twitter_id]
               if graph.has_edge(user_id, user2):
                  if 'twitter' not in graph[user_id][user2]['labels']:
                     graph[user_id][user2]['labels'].append('twitter')
               else:
                  graph.add_edge(user,friend)
                  graph[user_id][user2]['labels'] = ['twitter']
   return graph
sb_size = int(sys.argv[1])
hops = load_hops(sb_size)
graph = load_users_friends(hops, sb_size)
graph = load_users_tips(hops,graph)
graph = load_users_venues(hops,graph)
graph = load_twitter(hops, graph)

print "Source;Target;Label;Type"
for e in graph.edges():
    labels = ','.join(graph[e[0]][e[1]]['labels'])
    print "%s;%s;%s;Undirected" % (e[0],e[1],labels)
