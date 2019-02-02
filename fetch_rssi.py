import subprocess as sb
from time import sleep

def get_rssi():
    cmnd = " sudo iw wlp8s0 scan|egrep 'SSID|signal'"
    net = sb.Popen(cmnd, shell=True, stdout=sb.PIPE, stderr=sb.STDOUT)

    net_out = net.communicate()[0]
    net_out = net_out.decode('utf-8')
    net_out = net_out.strip('\n')
    net_out = net_out.split()
    ssid_pos = net_out.index('OnePlus')
    rssi_value = net_out[ssid_pos - 3]
    print(rssi_value)
    rssi_value = float(rssi_value)
    return rssi_value

if __name__ == "__main__":
    while True:
        try:
            get_rssi()
        except ValueError:

            print("registered ssid not found here")
            sleep(5)
            pass



