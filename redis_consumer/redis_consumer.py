import redis
import plotext as plt
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

logger.info("Starting consumer")
r = redis.Redis(host='localhost', port=6379)

# Read data from Redis stream
stream_name = 'your_stream_name'
last_id = '0'  # Start reading from the beginning of the stream

response = r.xread({stream_name: last_id}, block=0)
print(type(response))


import json

# Assuming 'response' is the data you received from Redis
combined_data_list = []  # Initialize an empty list to hold all data

for stream in response:
    stream_name = stream[0].decode('utf-8')
    messages = stream[1]

    for message in messages:
        message_id = message[0].decode('utf-8')
        data = message[1]

        if b'data' in data:
            # Decode bytes to string and parse JSON
            data_list = json.loads(data[b'data'].decode('utf-8'))

            # Extend the combined list with this data list
            combined_data_list.extend(data_list)

# Now 'combined_data_list' contains all the data from all messages
print(combined_data_list)



import matplotlib.pyplot as plt

# Assuming 'combined_data_list' is the data you want to plot
plt.plot(combined_data_list)
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Plot of Combined Data List')
plt.show()

