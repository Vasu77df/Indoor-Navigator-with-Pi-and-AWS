import boto3
from boto3.dynamodb.conditions import Key, Attr

ddb = boto3.resource('dynamodb',
                     region_name='eu-west-1'
                     )

table_one = ddb.Table('threeBdataTable')
table_two = ddb.Table('threeDataTable')
table_three = ddb.Table('zeroDataTable')
response_one = table_one.scan(
    FilterExpression=Attr('now_time').between(1552565040980, 1552565087912)
)


response_two = table_two.scan(
    FilterExpression=Attr('now_time').between(1552565037028, 1552565074419)
)

response_three = table_three.scan(
    FilterExpression=Attr('now_time').between(1552565046449, 1552565080265)
)
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


items_one = response_one['Items']
rssi_list_one = value_extractor(items_one)
print(rssi_list_one)
items_two = response_two['Items']
rssi_list_two = value_extractor(items_two)
print(rssi_list_two)
items_three = response_three['Items']
rssi_list_three = value_extractor(items_three)
print(rssi_list_three)
