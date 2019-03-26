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
    print(rssi_threeB)
    print(rssi_three)
    print(rssi_zero)

    return rssi_threeB, rssi_three, rssi_zero


def rssi_alogrithm():
    a, b, c = table_accessor()
    location = ""
    if a >= 20 and a <= 50:
        if b >= 60 and a <= 85:
            if c >= 40 and c <= 75:
                location = "thirteen zero five"

    elif c >= 20 and c <= 55:
        if b >= 65 and b <= 100:
            if a >= 50 and a <= 65:
                location = "thirteen zero four"

    elif b >= 20 and b <= 60:
        if c >= 70 and c <= 100:
            if a >= 50 and a <= 75:
                location = "thirteen zero six"
    else:
        location = "nowhere"

    return location

if __name__ == '__main__':
    loc = rssi_alogrithm()
    print("you are in the " + loc)