import logging
import time
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

import boto3
from boto3.dynamodb.conditions import Attr
from statistics import mean

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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

    items_two = response_two['Items']
    rssi_list_two = value_extractor(items_two)

    items_three = response_three['Items']
    rssi_list_three = value_extractor(items_three)


    rssi_threeb, rssi_three, rssi_zero = averager(rssi_list_one, rssi_list_two, rssi_list_three)

    return rssi_threeb, rssi_three, rssi_zero


def rssi_alogrithm():
    a, b, c = table_accessor()
    print("average value of threeB node:\t" + str(a))
    print("average value of pi three node:\t" + str(b))
    print("average value of pi zero node:\t" + str(c))
    location = ""
    if a >= 20 and a <=35:
        if b >= 80 and a <= 95:
            if c >= 65 and a <= 78:
                location = "bedroom"
    else:
        location = "nowhere"

    return location


class CurrentLocationAndLaunchHandler(AbstractRequestHandler):
    """Handler for skill launch and CurrentLocation"""

    def can_handle(self, handler_input):
        return (is_request_type("LaunchRequest")(handler_input) or
                is_intent_name("CurrentLocationIntent")(handler_input))

    def handle(self, handler_input):
        location = current_loc_finder()
        speech =  "Right now you are in " + location

        handler_input.response_builder.speak(speech).set_card(SimpleCard(speech))\
            .set_should_end_session(True)

        return handler_input.response_builder.response


class NavigationHandler(AbstractRequestHandler):
    """Handler for Navigating to other rooms """

    def can_handle(self, handler_input):
        return is_intent_name("NavigationIntent")(handler_input)

    def handle(self, handler_input):
        location = current_loc_finder()
        slots = handler_input.request_envelope.request.intent.slots
        current_place = slots["class_no"].value
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


