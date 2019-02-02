import rssi
interface = 'wlp8s0'
rssi_scanner = rssi.RSSI_Scan(interface)
ssids = ['OnePlus']

ap_info = rssi_scanner.getAPinfo(sudo=True)
print(ap_info)


