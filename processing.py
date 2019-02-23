from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import time
import json
import subprocess as sb
from time import sleep
from statistics import mean

def value_extracter(rssi_value):
    rssi_value = rssi_value.decode('utf-8')
    rssi_value = json.loads(rssi_value)
    rssi_value = rssi_value["rssi_value"]
    rssi_value = float(rssi_value)
    return rssi_value

# Custom Shadow callback
def customShadowCallback_Update(payload, responseStatus, token):
    # payload is a JSON string ready to be parsed using json.loads(...)
    # in both Py2.x and Py3.x
    if responseStatus == "timeout":
        print("Update request " + token + " time out!")
    if responseStatus == "accepted":
        payloadDict = json.loads(payload)
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        print("Update request with token: " + token + " accepted!")
        print("property: " + str(payloadDict["state"]["desired"]["property"]))
        print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    if responseStatus == "rejected":
        print("Update request " + token + " rejected!")

def customShadowCallback_Delete(payload, responseStatus, token):
    if responseStatus == "timeout":
        print("Delete request " + token + " time out!")
    if responseStatus == "accepted":
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        print("Delete request with token: " + token + " accepted!")
        print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    if responseStatus == "rejected":
        print("Delete request " + token + " rejected!")


def customCallback(client, userdata, message):
    node_one = None
    node_two = None
    if message.topic == "rssi/zero":
        node_one = value_extracter(message.payload)
        print("node one value: %s" % node_one)
    elif message.topic == "rssi/three":
        node_two = value_extracter(message.payload)
        print("node two value: %s" % node_two)

rootCAPath = "root-CA.crt"
certificatePath = "PiThreeBNode.cert.pem"
privateKeyPath = "PiThreeBNode.private.key"
thingName = "PiThreeBNode"

# Init AWSIoTMQTTShadowClient

myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient("clientId")
myAWSIoTMQTTShadowClient.configureEndpoint("a1jgcb96hr49vu-ats.iot.eu-west-1.amazonaws.com", 8883)
myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
myMQTTClient = myAWSIoTMQTTShadowClient.getMQTTConnection()

# Connect to AWS IoT
myAWSIoTMQTTShadowClient.connect()

# Create a deviceShadow with persistent subscription
deviceShadowHandler = myAWSIoTMQTTShadowClient.createShadowHandlerWithName(thingName, True)

# Delete shadow JSON doc
deviceShadowHandler.shadowDelete(customShadowCallback_Delete, 5)

while True:
    # subsribing to topic
    myMQTTClient.subscribe("rssi/#", 1, customCallback)
    time.sleep(1)
