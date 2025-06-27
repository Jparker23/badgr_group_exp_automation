import http.client
import json

# enter Bearer tokens
Bearer = ""

# establish secure HTTPS connection to badgr API
conn = http.client.HTTPSConnection("api.badgr.io")
payload = ''

# set authorization header using earlier set bearer token
headers = {
  'Authorization': f'Bearer {Bearer}'
}

# send a get request to get all badge classes
conn.request("GET", "/v2/badgeclasses", payload, headers)
# get response
res = conn.getresponse()
#read the raw data
data = res.read()

# initialize a counter for unique badge classes
num_unique_classes = 0

# decode data into UTF-8 string
decoded_data = data.decode("utf-8")

# Split string by commas
seperated_entries = decoded_data.split(",")

# List to stre the entityID lines
all_classes = []

# find lines containing entityID and store them
for item in seperated_entries:
    if "\"entityId\":" in item:
        all_classes.append(item)
        
# convert list to a set to remove duplicates
unique_classes = set(all_classes)

# get number of unique classes and print it
for item in unique_classes:
    num_unique_classes += 1
print(num_unique_classes)    

# close HTTPS connection
conn.close
