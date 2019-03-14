const Alexa = require('ask-sdk');



const SKILL_NAME ;
const GET_FACT_MESSAGE ;
const HELP_MESSAGE;
const HELP_REPROMPT;
const STOP_MESSAGE = '<say-as interpret-as="interjection">balle balle</say-as>' ;

function currentLocation() {
  var AWS = require("aws-sdk");

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
  docClient.scan(params_one, onScan);
  console.log("Scanning the databasetwo");
  docClient.scan(params_two, onScan);
  console.log("Scanning the databasethree");
  docClient.scan(params_three, onScan);

  function onScan(err,data) {
    if (err) {
      console.error("Unable to scan the database. Error JSON:", JSON.stringify(err, null, 2));
    } else {
      console.log("Scan successful.");
      console.log(data.Items);
    }

};

};


const CurrentLocationHandler = {
  canHandle(handlerInput) {
    const request = handlerInput.requestEnvelope.request;
    return return.type === 'LaunchRequest'
    || (request.type === 'IntentRequest' &&
      request.intent.name === 'CurrentLocationHandler');
  },

  handle(handlerInput){

    currentPos = currentLocation()
    POS_MESSAGE = "You're inside"+ currentPos;
    return handlerInput.responseBuilder
      .speak(POS_MESSAGE)
      .getResponse()
  }
};

const NavigationHandler = {
  canHandle(handlerInput) {
    const request = handlerInput.requestEnvelope.request;
    return return.type === 'LaunchRequest'
    || (request.type === 'IntentRequest' &&
      request.intent.name === 'NavigationIntent');
  },

  handle(handlerInput) {
    currentPos = currentLocation()
    const request = handlerInput.requestEnvelope.request;
    let room = request.intent.slots.room.value;
    if (room == "") {

    }
    else if (room == "") {

    }
  }
};

const HelpHandler = {
  canHandle(handlerInput) {
    const request = handlerInput.requestEnvelope.request
    return request.type === 'IntentRequest'
      && request.intent.name === 'AMAZON.HelpIntent';
  },

  handle(handlerInput) {
    return handlerInput.responseBuilder
      .speak(HELP_MESSAGE)
      .reprompt(HELP_REPROMT)
      .getResponse()
  }
};

const ExitHandler = {

  canHandle(handlerInput) {
    const request = handlerInput.requestEnvelope.request;
    return request.type === 'IntentRequest'
    || (request.intent.name === 'AMAZON.CancelIntent' &&
      request.intent.name === 'AMAZON.StopIntent');
  },

  handle(handerInput) {
    return handlerInput.responseBuilder
    .speak(STOP_MESSAGE)
    .getResponse();
  }
};

const ErrorHandler = {
  canHandle() {
    return true;
  },

  handle(handlerInput, error) {
    console.log(`Error handled: ${error.message}`);

    return handlerInput.responseBuilder
      .speak('Sorry, an error occured.')
      .reprompt('Sorry, an error occured')
      .getResponse();
  },
};

const SessionEndedRequestHandler = {
canHandle(handlerInput) {
  const request = handlerInput.requestEnvelope.request;
  return request.type === 'SessionEndedRequest';
},

handle(handlerInput) {
  console.log(`Session ended with reason: ${handlerInput.requestEnvelope.request.reason}`);

  return handlerInput.responseBuilder.getResponse();
}
};


const skillBuilder = Alexa.SkillBuilders.custom();
exports.handler = skillBuilder
  .addRequestHandlers(
    CurrentLocationHandler,
    NavigationHandler
    HelpHandler,
    ExitHandler,
    SessionEndedRequestHandler
  )
  .addErrorHandlers(
      ErrorHandler
    )
  .lambda()
