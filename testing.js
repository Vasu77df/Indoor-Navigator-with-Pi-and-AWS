var AWS = require("aws-sdk");
var now_time = require("microtime")

AWS.config.update({
 region: "eu-west-1",
 endpoint: "https://dynamodb.eu-west-1.amazonaws.com"
});

var docClient = new AWS.DynamoDB.DocumentClient();


var params_one = {
  TableName: "threeBdataTable",
  ProjectionExpression: "#ix, rssi_value_threeB, now_time",
  FilterExpression: "now_time between :first and :last",
  ExpressionAttributeNames: {
 "#ix": "index",
 },
  ExpressionAttributeValues: {
    ":first":1552565040980,
    ":last":1552565087912
  }
};

var params_two = {
  TableName: "threeDataTable",
  ProjectionExpression: "#ix, rssi_value_three, now_time",
  FilterExpression: "now_time between :first and :last",
  ExpressionAttributeNames: {
 "#ix": "index",
 },
  ExpressionAttributeValues: {
    ":first":1552565037028,
    ":last":1552565074419
  }
};

var params_three = {
  TableName: "zeroDataTable",
  ProjectionExpression: "#ix, rssi_value_zero, now_time",
  FilterExpression: "now_time between :first and :last",
  ExpressionAttributeNames: {
 "#ix": "index",
 },
  ExpressionAttributeValues: {
    ":first":1552565046449,
    ":last":1552565080265
  }
};

console.log("Scanning the databaseone");
docClient.scan(params_one, function(err, data) {
  if (err) {
    console.error("Unable to scan the database. Error JSON:", JSON.stringify(err, null, 2));
  } else {
    console.log("Scan successful.");
    console.log(data.Items);
  }
});
console.log("Scanning the databasetwo");
docClient.scan(params_two, function(err, data) {
  if (err) {
    console.error("Unable to scan the database. Error JSON:", JSON.stringify(err, null, 2));
  } else {
    console.log("Scan successful.");
    console.log(data.Items);
  }
});
console.log("Scanning the databasethree");
docClient.scan(params_three, function(err, data) {
  if (err) {
    console.error("Unable to scan the database. Error JSON:", JSON.stringify(err, null, 2));
  } else {
    console.log("Scan successful.");
    console.log(data.Items);
  }
});
