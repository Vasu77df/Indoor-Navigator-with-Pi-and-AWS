from math import pow, sqrt
from fetch_rssi import get_rssi
def distance_calc():
    tx = -35
    rssi = get_rssi()
    ratio = tx - rssi
    ratio_lin = pow(10, ratio/10)

    d = sqrt(ratio_lin)
    print(d)

if __name__ == '__main__':
    distance_calc()
