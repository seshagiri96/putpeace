#!/usr/bin/python

from twitter import *
import re

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

#-----------------------------------------------------------------------
# load our API credentials from a file config.py
#
# consumer_key = "XxXxXxxXXXxxxxXXXxXX"
#consumer_secret = "xXXXXXXXXxxxxXxXXxxXxxXXxXxXxxxxXxXXxxxXXx"
#access_key = "XXXXXXXX-xxXXxXXxxXxxxXxXXxXxXxXxxxXxxxxXxXXxXxxXX"
#access_secret = "XxXXXXXXXXxxxXXXxXXxXxXxxXXXXXxXxxXXXXx"
#
#
#-----------------------------------------------------------------------
config = {}
execfile("config.py", config)

#-----------------------------------------------------------------------
# create twitter API object
#-----------------------------------------------------------------------
twitter = Twitter(
		        auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))


#-----------------------------------------------------------------------
# perform a basic search 
#
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
# file to write our results
out_file = open('search_results.tx','w')
#-----------------------------------------------------------------------

# keep a count of our results
count = 0

query = twitter.search.tweets(q = "haircut",count=100)

# limit problem is solved by remembering the last id in our previous results and using it as
# upper limit in our next query
max_id = query["statuses"][-1]["id"]

for result in query["statuses"]:
	line = result["text"]
	line = re.sub(r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+','',line)
	line = re.sub(r'(?:@[\w_]+)','',line)
	line = re.sub(r'#',' ',line)
	line = re.sub(emoticons_str,'',line)
	line = re.sub(r'RT|:','',line)
	
	for char in line:
		try:
			out_file.write(char)
		except:
			pass
	out_file.write('\n')

#-----------------------------------------------------------------------
# Loop through each of the results, and print its content.
#-----------------------------------------------------------------------
while count > 1000:
	query = twitter.search.tweets(q = "haircut",count=100,max_id=max_id)
	count += len(query["statuses"])
	max_id = query["statuses"][-1]["id"]
	for result in query["statuses"]:
		out_file.write(result["text"]+'\n')

out_file.close()