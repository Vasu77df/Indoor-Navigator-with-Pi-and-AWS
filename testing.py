import boto3
from boto3.dynamodb.conditions import Key, Attr

ddb = boto3.resource('dynamodb',
                     region_name='eu-west-1'
                     )

table_one = ddb.Table('threeBdataTable')
table_two = ddb.Table('threeDataTable')
table_there = ddb.Table('zeroDataTable')
response_one = table_one.scan(
    FilterExpression=Attr('now_time').between(1552565040980, 1552565087912)
)


response_two = table_one.scan(
    FilterExpression=Attr('now_time').between(1552565037028, 1552565074419)
)

response_three = table_one.scan(
    FilterExpression=Attr('now_time').between(1552565046449, 1552565080265)
)


print(len(response_one['Items']))
print(response_two['Items'])
print(response_three['Items'])
