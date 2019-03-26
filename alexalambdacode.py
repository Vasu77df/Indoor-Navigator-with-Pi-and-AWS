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


def current_loc_finder():
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


class CurrentLocationAndLaunchHandler(AbstractRequestHandler):
    """Handler for skill launch and CurrentLocation"""

    def can_handle(self, handler_input):
        return (is_request_type("LaunchRequest")(handler_input) or
                is_intent_name("CurrentLocationIntent")(handler_input))

    def handle(self, handler_input):
        location = current_loc_finder()
        speech = "Right now you are near" + " " + location

        handler_input.response_builder.speak(speech).set_card(SimpleCard("My Locator:", speech))\
            .set_should_end_session(False)

        return handler_input.response_builder.response


class NavigationHandler(AbstractRequestHandler):
    """Handler for Navigating to other rooms """

    def can_handle(self, handler_input):
        return is_intent_name("NavigationIntent")(handler_input)

    def handle(self, handler_input):
        location = current_loc_finder()
        slots = handler_input.request_envelope.request.intent.slots
        desired_location = int(slots["classnumber"].value)

        from_1304__1305 = "Right now you are near thirteen zero four, exit thirteen zero four and thirteen zero five will be the next room to your right."
        from_1304__1306 = "Right now you are near thirteen zero four, exit thirteen zero four and thirteen zero six will be the second room to your right."
        from_1304__1204 = "Right now you are near thirteen zero four,"
        from_1304__1205 = "Right now you are near thirteen zero four,"
        from_1304__1206 = "Right now you are near thirteen zero four,"

        from_1305__1304 = "Right now you are near thirteen zero five, exit thirteen zero five and thirteen zero four will be the next room to your left."
        from_1305__1306 = "Right now you are near thirteen zero five, exit thirteen zero five and thirteen zero six will be the next room to your right."
        from_1305__1204 = "Right now you are near thirteen zero five,"
        from_1305__1205 = "Right now you are near thirteen zero five,"
        from_1305__1206 = "Right now you are near thirteen zero five,"

        from_1306__1304 = "Right now you are near thirteen zero six,"
        from_1306__1305 = "Right now you are near thirteen zero six,"
        from_1306__1204 = "Right now you are near thirteen zero six,"
        from_1306__1205 = "Right now you are near thirteen zero six,"
        from_1306__1206 = "Right now you are near thirteen zero six,"

        if location == "thirteen zero four":
            if desired_location == 1305:
                handler_input.response_builder.speak(from_1304__1305).set_card(SimpleCard("My Locator:", from_1304__1305))\
                    .set_should_end_session(False)
                return handler_input.response_builder.response
            elif desired_location == 1306:
                handler_input.response_builder.speak(from_1304__1306).set_card(SimpleCard("My Locator:", from_1304__1306))\
                    .set_should_end_session(False)
                return handler_input.response_builder.response
            elif desired_location == 1204:
                handler_input.response_builder.speak(from_1304__1204).set_card(SimpleCard("My Locator:", from_1304__1204))\
                    .set_should_end_session(False)
                return handler_input.response_builder.response
            elif desired_location == 1205:
                handler_input.response_builder.speak(from_1304__1205).set_card(SimpleCard("My Locator:", from_1304__1205))\
                    .set_should_end_session(False)
                return handler_input.response_builder.response
            elif desired_location == 1206:
                handler_input.response_builder.speak(from_1304__1206).set_card(SimpleCard("My Locator:", from_1304__1206))\
                    .set_should_end_session(False)
                return handler_input.response_builder.response
            else:
                handler_input.response_builder.speak("you cannot go from thirteen zero four to this place right now") \
                    .set_should_end_session(False)
                return handler_input.response_builder.response

        if location == "thirteen zero five":
            if desired_location == 1304:
                handler_input.response_builder.speak(from_1305__1304).set_card(SimpleCard("My Locator:", from_1305__1304))\
                    .set_should_end_session(False)
                return handler_input.response_builder.response
            elif desired_location == 1306:
                handler_input.response_builder.speak(from_1305__1306).set_card(SimpleCard("My Locator:", from_1305__1306))\
                    .set_should_end_session(False)
                return handler_input.response_builder.response
            elif desired_location == 1204:
                handler_input.response_builder.speak(from_1305__1204).set_card(SimpleCard("My Locator:", from_1305__1204))\
                    .set_should_end_session(False)
                return handler_input.response_builder.response
            elif desired_location == 1205:
                handler_input.response_builder.speak(from_1305__1205).set_card(SimpleCard("My Locator:", from_1305__1205))\
                    .set_should_end_session(False)
                return handler_input.response_builder.response
            elif desired_location == 1206:
                handler_input.response_builder.speak(from_1305__1206).set_card(SimpleCard("My Locator:", from_1305__1206))\
                    .set_should_end_session(False)
                return handler_input.response_builder.response
            else:
                handler_input.response_builder.speak("you cannot go from thirteen zero five to this place right now") \
                    .set_should_end_session(False)
                return handler_input.response_builder.response

        if location == "thirteen zero six":
            if desired_location == 1304:
                handler_input.response_builder.speak(from_1306__1304).set_card(SimpleCard("My Locator:", from_1306__1304))\
                    .set_should_end_session(False)
                return handler_input.response_builder.response
            elif desired_location == 1305:
                handler_input.response_builder.speak(from_1306__1305).set_card(SimpleCard("My Locator:", from_1306__1305))\
                    .set_should_end_session(False)
                return handler_input.response_builder.response
            elif desired_location == 1204:
                handler_input.response_builder.speak(from_1306__1204).set_card(SimpleCard("My Locator:", from_1306__1204))\
                    .set_should_end_session(False)
                return handler_input.response_builder.response
            elif desired_location == 1205:
                handler_input.response_builder.speak(from_1306__1205).set_card(SimpleCard("My Locator:", from_1306__1205))\
                    .set_should_end_session(False)
                return handler_input.response_builder.response
            elif desired_location == 1206:
                handler_input.response_builder.speak(from_1306__1206).set_card(SimpleCard("My Locator:", from_1306__1206))\
                    .set_should_end_session(False)
                return handler_input.response_builder.response
            else:
                handler_input.response_builder.speak("you cannot go from thirteen zero six to this place right now") \
                    .set_should_end_session(False)
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
        speech_text = "You can ask me, where am I right now ,or to help you navigate to another location"

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

        speech_text = "Goodbye and Good luck, may the force be with you!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Indoor Locator:", speech_text))
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
            "The My Locator skill can't help you with that.  "
            "You can say where am I?")
        reprompt = "You can say which room am I in ?"
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

        speech = "Sorry, there was some problem in My Locator. Please try again!!"
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


