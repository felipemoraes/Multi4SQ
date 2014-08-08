Multi4SQ
========

In this project was developed some scripts to get data from Foursquare social network using its public API. This is part of my work during my internship at Mitacs Globalink program. This scrips yields an output with a CSV format with multidimension network as this describe here: http://goo.gl/Br70ot


NOTE: This is beta version, it's still in tests and require access tokens from Foursquare API and Twitter API. 

How to use this scripts:

First at all, this scripts uses a lot of sockets and was only tested on UNIX environments. 


1) Two scripts needs to be running until all the data is been collected. Run 'python server.py #hops', #hops is the number of hops do you wanna from a random user. The other command is 'python access.py' and also needs to be running until the data is been collected.

2) Run 'python start.py', this script will take some time. This script get a random user from Twitter that checked-in in some place.

3) After run 'python client.py', this also take some time and I recommend put its in background.

4) Then run 'python twitter.py', this also take much more time because have to access Twitter API and get users friends (60 seconds for each user). 

5) To finish, parse all data with the command 'python extract.py #hops >output.csv', this yields an CSV file that content a Multidimensional Network of Foursquare.

Please, as is a Beta version I still have to do a lot of improvements. I will be glad if you contact me describing all my mistakes and errors.


