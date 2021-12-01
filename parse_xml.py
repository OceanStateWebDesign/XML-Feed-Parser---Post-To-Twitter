import xml.etree.ElementTree as ET
import requests
import hashlib
import os
import sys
import tweepy

auth = tweepy.OAuthHandler("APIKEY", "APISECRET")
auth.set_access_token("APITOKEN", "APISECRET")

#Variable sets the python hash seed to 0, therefore we recieve consistent hash results.(By default the seed rotates per execution)
hashseed = os.getenv('PYTHONHASHSEED')

#Make sure we have the hashseed env
if not hashseed:
    os.environ['PYTHONHASHSEED'] = '0'
    os.execv(sys.executable, [sys.executable] + sys.argv)

#Set the XML File/Feed to pull
tree = ET.fromstring(requests.get('https://example.com/feed/').text)


#For each title node
for item in tree.iter('item'):

	#Define the post title
	title = item.find('title')

	#Define the post url
	link = item.find('link')

	#create a unique 8 digit hash as an ID based on the title
	id = str(hash(title.text) % 10**8)

	#see if ID is found in db.txt
	with open('db.txt') as file:

		#if the ID is found
		if id in file.read():

			#Do this if found
			print('ID Found In DataBase' + id)

		else:

			#Do this if ID is not found
			print("ID not found " + id)
			print("Title: " + title.text)
			print("Link: " + link.text)

			#Initialize Sending Tweet
			api = tweepy.API(auth)

			#Here we are posting the post title & link to twitter.
			api.update_status(title.text + " " + link.text)

			#Record current id to database file so its not reported on again
			newdb = open('db.txt', 'a')
			newdb.write(id + "\n")
			newdb.close()
