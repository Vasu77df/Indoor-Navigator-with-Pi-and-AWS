import boto3
from boto3.dynamodb.conditions import Key, Attr

ddb = boto3.resource('dynamodb',
                     region_name='eu-west-1'
                     )


table = ddb.Table('threeBdataTable')

response = table.scan(
    FilterExpression=Attr('time').between(1551008923506, 1551008966690)
)


item = response['Items']

print(item)
print(type(item))
