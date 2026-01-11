import time
import paho.mqtt.client as mqtt
from pathlib import Path

class AWSIoTClient:
    def __init__(self, endpoint, client_id, topic, root_ca, certfile, keyfile):

        self.topic = topic
        self.connected = False

        self.client = mqtt.Client(client_id=client_id)
        self.client.tls_set(
            ca_certs=str(Path(root_ca)),
            certfile=str(Path(certfile)),
            keyfile=str(Path(keyfile))
        )

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

        self.client.loop_start()
        self.client.connect(endpoint, 8883)

        while not self.connected:
            time.sleep(0.1)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("MQTT connected successfully")
            self.connected = True
        else:
            print(f"MQTT connection failed, rc={rc}")

    def on_disconnect(self, client, userdata, rc):
        print(f"MQTT disconnected, rc={rc}")
        self.connected = False
    
    def publish(self, payload, timeout=5):

        if not self.connected:
            raise RuntimeError("MQTT client is not connected")
        
        try:
            msg_info = self.client.publish(self.topic, payload, qos=1)

            if msg_info.rc != mqtt.MQTT_ERR_SUCCESS:
                raise RuntimeError(
                    f"Publish failed immediately, rc={msg_info.rc}"
                )

        except Exception as e:
            raise RuntimeError(f"MQTT publish failed: {e}")

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
        print("MQTT client disconnected")
        