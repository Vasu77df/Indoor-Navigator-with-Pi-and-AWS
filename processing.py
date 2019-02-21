from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import time
import json
from statistics import mean

def topic_filter(rssi_value):
    rssi_value = rssi_value.decode('utf-8')
    rssi_value = json.loads(rssi_value)
    rssi_value = rssi_value["rssi_zero_node"]
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
    if message.topic == "rssi/zero":
        rssi_value = topic_filter(message.payload)
        rssi_val_zeronode = rssi_value
    elif message.topic == "rssi/three":
        rssi_value = topic_filter(message.payload)
        rssi_val_threenode = rssi_value
    processing(rssi_val_zeronode, rssi_val_threenode)


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

def processing(rssi_one, rssi_two):
    x = []
    y = []
    if len(x) == 11:
        x.clear()
    if len(y) == 11:
        x.clear()
    x.append(rssi_one)
    y.append(rssi_one)
    node_one = mean(x)
    node_two = mean(y)
    print(node_one)
    print(node_two)


while True:
    myMQTTClient.subscribe("rssi/#", 1, customCallback)
    time.sleep(1)