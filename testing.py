from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time



rootCAPath = "root-CA.crt"
certificatePath = "PiZeroNode.cert.pem"
privateKeyPath = "PiZeroNode.private.key"
topic = "zero/node"


def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    rssi_value = message.payload
    print
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


myAWSIoTMQTTClient = AWSIoTMQTTClient("myClientID")
myAWSIoTMQTTClient.configureEndpoint("a1jgcb96hr49vu-ats.iot.eu-west-1.amazonaws.com", 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()


while True:
    myAWSIoTMQTTClient.subscribe("three/node", 1, customCallback)

    time.sleep(1)
