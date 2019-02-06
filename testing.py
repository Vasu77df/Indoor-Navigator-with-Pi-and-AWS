from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json


rootCAPath = "root-CA.crt"
certificatePath = "PiZeroNode.cert.pem"
privateKeyPath = "PiZeroNode.private.key"
topic = "zero/node"


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

# Publish to the same topic in a loop forever
loopCount = 0
while True:
    message = {"loopCount": loopCount}
    messageJson = json.dumps(message)
    myAWSIoTMQTTClient.publish(topic, messageJson, 1)
    print('Published topic %s: %s\n' % (topic, messageJson))
    loopCount += 1
    time.sleep(1)
