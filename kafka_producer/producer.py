import logging
from kafka import KafkaProducer
import numpy as np
import json
import time

# Configure the logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

producer = KafkaProducer(bootstrap_servers=['kafka:9092'], value_serializer=lambda x: json.dumps(x).encode('utf-8'))

while True:
    try:
        data = np.random.rand(50).tolist()
        producer.send('your_topic', value=data)
        logger.info("Data sent successfully")
        time.sleep(1)
    except Exception as e:
        logger.error(f"Error sending data: {str(e)}")
