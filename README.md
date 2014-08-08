Multi4SQ
========

In this project was developed some scripts to get data from Foursquare social network using its public API. This is part of my work during my internship at Mitacs Globalink program. This scrips yields an output with a CSV format with multidimension network as this describe here: http://goo.gl/Br70ot


NOTE: This is beta version, it's still in tests and require access tokens from Foursquare API and Twitter API. 

How to use this scripts:

First at all, this scripts uses a lot of sockets and was only tested on UNIX environments. The file 'access_keys' have to contains access tokens from Foursquare. To know how to get Foursquare access tokens visit: https://developer.foursquare.com/overview/auth. The twitter.py and start.py needs authentication keys from Twitter, to learn how to get it, follow this steps:
The steps below will help you set up your twitter account to be able to access the live 1% stream.

1) Create a twitter account if you do not already have one.
2) Go to https://dev.twitter.com/apps and log in with your twitter credentials.
3) Click "Create New App"
4) Fill out the form and agree to the terms. Put in a dummy website if you don't have one you want to use.
On the next page, click the "API Keys" tab along the top, then scroll all the way down until you see the section "Your Access Token"
5) Click the button "Create My Access Token". You can Read more about Oauth authorization.
You will now copy four values into twitter.py and start.py. These values are your "API Key", your "API secret", your "Access token" and your "Access token secret". All four should now be visible on the API Keys page. (You may see "API Key" referred to as "Consumer key" in some places in the code or on the web; they are synonyms.) Open twitter.py and and start.py set the variables corresponding to the api key, api secret, access token, and access secret. You will see code like the below:
api_key = "<Enter api key>"
api_secret = "<Enter api secret>"
access_token_key = "<Enter your access token key here>"
access_token_secret = "<Enter your access token secret here>"

1) Two scripts needs to be running until all the data is been collected. Run 'python server.py #hops', #hops is the number of hops do you wanna from a random user. The other command is 'python access.py' and also needs to be running until the data is been collected.

2) Run 'python start.py', this script will take some time. This script get a random user from Twitter that checked-in in some place.

3) After run 'python client.py', this also take some time and I recommend put its in background.

4) Then run 'python twitter.py', this also take much more time because have to access Twitter API and get users friends (60 seconds for each user). 

5) To finish, parse all data with the command 'python extract.py #hops >output.csv', this yields an CSV file that content a Multidimensional Network of Foursquare.

Please, as is a Beta version I still have to do a lot of improvements. I will be glad if you contact me describing all my mistakes and errors.


