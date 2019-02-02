import subprocess as sb
from time import sleep

def get_apinfo():
    cmnd = " sudo iw wlp8s0 scan|egrep 'SSID|signal'"
    net = sb.run(cmnd, shell=True, stdout=sb.PIPE, stderr=sb.STDOUT)

    net_out = net.stdout
    net_out = net_out.decode('utf-8')
    net_out = net_out.strip('\n')
    net_out = net_out.split()
    return net_out


def rssi_parser(net_out):
    reg_user = 'OnePlus'
    if reg_user in net_out:
        ssid_pos = net_out.index('OnePlus')
        rssi_value = net_out[ssid_pos - 3]
        rssi_value = float(rssi_value)
    else:
        rssi_value = 0
        sleep(5)
    return rssi_value

if __name__ == "__main__":
    while True:
        net_info = get_apinfo()
        rssi = rssi_parser(net_info)
        print(rssi)




