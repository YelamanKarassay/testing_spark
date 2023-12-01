# Use the Jupyter PySpark Notebook as a parent image
FROM jupyter/pyspark-notebook:latest


ADD https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.5.0/spark-sql-kafka-0-10_2.12-3.5.0.jar /spark/jars/

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .


# Install any additional packages if needed
# e.g., RUN pip install ...
RUN pip install redis
# Run consumer.py when the container launches
CMD ["spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0", "./consumer.py"]

