const Alexa = require('ask-sdk');
const aws =  require('aws-sdk');


const SKILL_NAME ;
const GET_FACT_MESSAGE ;
const HELP_MESSAGE;
const HELP_REPROMPT;
const STOP_MESSAGE = '<say-as interpret-as="interjection">balle balle</say-as>' ;

function currentLocation() {
    var dbb = new aws.DynamoDB({apiVersion: '2012-10-08'});

}


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
