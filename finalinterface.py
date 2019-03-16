import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

import boto3
from boto3.dynamodb.conditions import Key, Attr


sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def current_loc_finder():
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

    return location


class CurrentLocationAndLaunchHandler(AbstractRequestHandler):
    """Handler for skill launch and CurrentLocation"""

    def can_handle(self, handler_input):
        return (is_request_type("LaunchRequest")(handler_input) or
                is_intent_name("CurrentLocationIntent")(handler_input))

    def handle(self, handler_input):
        location = current_loc_finder()
        speech =  "Right now your in the" + location

        handler_input.response_builder.speak(speech).set_card(SimpleCard(speech))\
            .set_should_end_session(True)

        return handler_input.response_builder.response


class NavigationHandler(AbstractRequestHandler):
    """Handler for Navigating to other rooms """

    def can_handle(self, handler_input):
        return is_intent_name("NavigationIntent")(handler_input)

    def handle(self, handler_input):
        location = current_loc_finder()
        slots  =  handler_input.request_envelope.request.intent.slots
        current_place = slots["loaction"].value
        speech = ""

        if current_place == "":
            handler_input.response_builder.speak(speech).set_should_end_session(False)
            return handler_input.response_builder.response
        elif current_place == "":
            handler_input.response_builder.speak(speech).set_should_end_session(False)
            return handler_input.response_builder.response
        else:
            handler_input.response_builder.speak("I cannot help you navigate to this place right now")\
                .set_should_end_session(False)
            return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = "You can ask me where am I right now or to help you navigate to another location"

        handler_input.response_builder.speak(speech_text).ask(
            speech_text).set_card(SimpleCard(
                "Help:", speech_text))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):

        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Indoor Locator", speech_text))
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = (
            "The Hello World skill can't help you with that.  "
            "You can say hello!!")
        reprompt = "You can say hello!!"
        handler_input.response_builder.speak(speech_text).ask(reprompt)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):

        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        return handler_input.response_builder.response

class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):

        return True

    def handle(self, handler_input, exception):

        logger.error(exception, exc_info=True)

        speech = "Sorry, there was some problem. Please try again!!"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response


sb.add_request_handler(CurrentLocationAndLaunchHandler())
sb.add_request_handler(NavigationHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()


