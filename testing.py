from math import pow
from fetch_rssi import get_rssi
def distance_calc():
    tx = -22
    rssi = get_rssi()
    ratio = rssi*1.0/tx
    if ratio < 1.0:
        dis = pow(ratio, 10)
        print(dis)
    else:
        dis = 0.89976*pow(ratio, 7.7095) + 0.111
        print(dis)


if __name__ == '__main__':
    distance_calc()
