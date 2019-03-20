import boto3
from boto3.dynamodb.conditions import Attr
from statistics import mean
import time


def averager(x, y, z):
    avgx = mean(x)

    avgy = mean(y)

    avgz = mean(z)

    return abs(int(avgx)), abs(int(avgy)), abs(int(avgz))


def value_extractor(items):
    a = []
    for item in items:
        if 'rssi_value_threeB' in item.keys():
            value = float(item['rssi_value_threeB'])
            a.append(value)
        elif 'rssi_value_three' in item.keys():
            value = float(item['rssi_value_three'])
            a.append(value)
        elif 'rssi_value_zero' in item.keys():
            value = float(item['rssi_value_zero'])
            a.append(value)
        else:
            a.append(0)

    return a


def table_accessor():
    ddb = boto3.resource('dynamodb',
                         region_name='eu-west-1'
                         )

    table_one = ddb.Table('threeBdataTable')
    table_two = ddb.Table('threeDataTable')
    table_three = ddb.Table('zeroDataTable')
    now_time = int(round(time.time() * 1000))
    past_time = now_time - 40000
    response_one = table_one.scan(
        FilterExpression=Attr('now_time').between(past_time, now_time)
    )

    response_two = table_two.scan(
        FilterExpression=Attr('now_time').between(past_time, now_time)
    )

    response_three = table_three.scan(
        FilterExpression=Attr('now_time').between(past_time, now_time)
    )

    items_one = response_one['Items']

    rssi_list_one = value_extractor(items_one)
    print("list if scanned values for threeB node:" + str(rssi_list_one))
    items_two = response_two['Items']
    rssi_list_two = value_extractor(items_two)
    print("list of values scanned by pi three node:" + str(rssi_list_two))
    items_three = response_three['Items']
    rssi_list_three = value_extractor(items_three)
    print("list of values scanned by pi zero node:" + str(rssi_list_three))

    rssi_threeB, rssi_three, rssi_zero = averager(rssi_list_one, rssi_list_two, rssi_list_three)

    return rssi_threeB, rssi_three, rssi_zero


def rssi_alogrithm():
    a, b, c = table_accessor()
    print("average value of threeB node:\t" + str(a))
    print("average value of pi three node:\t" + str(b))
    print("average value of pi zero node:\t" + str(c))
    location = ""

    if a >= 20 and a <= 45:
        if b >= 80 and a <= 95:
            if c >= 60 and a <= 78:
                location = "bedroom"

    elif c >= 20 and c <= 45:
        if b >= 50 and b <= 75:
            if a >= 75 and a <= 95:
                location = "middle bedroom"

    elif b >= 15 and b <= 55:
        if c >= 55 and c <= 75:
            if a >=75 and a<=100:
                location = "hall"
    else:
        location = "nowhere"

    return location


if __name__ == '__main__':
    loc = rssi_alogrithm()
    print("you are in the " + loc)