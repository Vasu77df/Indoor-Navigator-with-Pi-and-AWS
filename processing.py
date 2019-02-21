from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import time
import json

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
    print("Received a new message: ")
    print(message.payload)
    rssi_value = message.payload
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


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

# Subcribe to other nodes and process the data and update device shadow for ALexa

while True:
    myMQTTClient.subscribe()