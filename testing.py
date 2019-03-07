import boto3

dynamodb = boto3.resource('dynamodb')

threeBtable = dynamodb.Table('threeBdataTable')
zerotable = dynamodb.Table('zeroDataTable')

response = threeBtable.get_item(
    Key={
         'index': 11
    }
)

response_two = zerotable.get_item(
    Key={
         'index': 11
    }
)

item = response['Item']
item_two = response_two['Item']
print(item)
print(item_two)