from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import subprocess as sb
from time import sleep

#authentication information and topic name
rootCAPath = "root-CA.crt"
certificatePath = "PiThreeBNode.cert.pem"
privateKeyPath = "PiThreeBNode.private.key"
topic = "rssi/threeB"

#getting rssi values from nearby devices
def get_apinfo():
    '''scans all available wifi networks and returns a list of the ssids and rssi
     values'''
    cmnd = " sudo iw wlan0 scan|egrep 'SSID|signal'"
    net = sb.run(cmnd, shell=True, stdout=sb.PIPE, stderr=sb.STDOUT)

    net_out = net.stdout
    net_out = net_out.decode('utf-8')
    net_out = net_out.strip('\n')
    net_out = net_out.split()
    return net_out

#filtering the rssi value for only registered ssid
def rssi_parser(net_out):
    ''' parses the list and filters only the rssi value of registered ssid '''

    reg_user = 'OnePlus'
    if reg_user in net_out:
        ssid_pos = net_out.index('OnePlus')
        rssi_value = net_out[ssid_pos - 3]
        rssi_value = float(rssi_value)
    else:
        rssi_value = 0
        sleep(5)
    return rssi_value


#Authenticating connection to AWS IoT
myAWSIoTMQTTClient = AWSIoTMQTTClient("myClientID")
myAWSIoTMQTTClient.configureEndpoint("a1jgcb96hr49vu-ats.iot.eu-west-1.amazonaws.com", 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect to AWS IoT
myAWSIoTMQTTClient.connect()
# Publish to the same topic in a loop forever
index = 0
while True:
    net_info = get_apinfo()
    rssi = rssi_parser(net_info)
    milli = int(round(time.time()*1000))
    index += 1
    message = {"index": index,
                "rssi_value_zero": rssi,
                "time": milli}
    messageJson = json.dumps(message)
    myAWSIoTMQTTClient.publish(topic, messageJson, 1)
    print('Published topic %s: %s\n' % (topic, messageJson))
    time.sleep(2)
