from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import time
import logging
import redis
from pyspark.sql import Row

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

def process_row(df, epoch_id):
    # Process and print the DataFrame
    if df.count() > 0:
        logger.info("Received data:")
        df.show(truncate=False)

        # Convert DataFrame to RDD and then to a list of Rows
        rows = df.rdd.map(lambda row: row.asDict()).collect()

        # Create a Redis connection
        r = redis.Redis(host='host.docker.internal', port=6379)

        # Stream name
        stream_name = 'your_stream_name'

        for row in rows:
            # Convert Row to a flat dictionary
            row_dict = {str(k): str(v) for k, v in row.items()}
            # Add data to Redis stream
            r.xadd(stream_name, row_dict)
            
spark = SparkSession.builder \
    .appName("KafkaSparkConsumer") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
    .config("spark.redis.host", "host.docker.internal") \
    .config("spark.redis.port", "6379") \
    .getOrCreate()

# Define your schema
schema = ArrayType(DoubleType())

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "your_topic") \
    .load() \
    .select(from_json(col("value").cast(StringType()), schema).alias("data"))

# Set the trigger for once a minute
query = df.writeStream \
    .foreachBatch(process_row) \
    .trigger(processingTime='1 minute') \
    .start()

query.awaitTermination()
