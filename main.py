import time
import json
import os
from dotenv import load_dotenv
from mqtt_client import AWSIoTClient
from particle_sensor import ParticleSensor

load_dotenv()

AWS_ENDPOINT = os.getenv("AWS_ENDPOINT")
CLIENT_ID = os.getenv("CLIENT_ID")
TOPIC = os.getenv("TOPIC")
ROOT_CA = os.getenv("ROOT_CA")
CERTFILE = os.getenv("CERTFILE")
KEYFILE = os.getenv("KEYFILE")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 10))
BATCH_INTERVAL = int(os.getenv("BATCH_INTERVAL", 300))
READ_INTERVAL = float(os.getenv("READ_INTERVAL", 1))

sensor = ParticleSensor()
aws_client = AWSIoTClient(AWS_ENDPOINT, CLIENT_ID, TOPIC, ROOT_CA, CERTFILE, KEYFILE)

batch = []
last_send_time = time.time()

try:
    while True:
        reading = sensor.read()
        batch.append(reading)
        print(f"Collected reading: {reading}")

        time_since_last_send = time.time() - last_send_time
        # Send batch if size or failsafe time threshold is met
        if len(batch) >= BATCH_SIZE or time_since_last_send >= BATCH_INTERVAL:
            payload = json.dumps(batch)
            aws_client.publish(payload)
            print(f"Published batch of {len(batch)} readings to AWS IoT")
            batch = []
            last_send_time = time.time()

        time.sleep(READ_INTERVAL)

except KeyboardInterrupt:
    print("Exiting program...")
    aws_client.disconnect()
