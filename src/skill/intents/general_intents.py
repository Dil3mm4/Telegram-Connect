from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name

from src.skill.i18n.language_model import LanguageModel
from src.skill.utils.exceptions import respond_to_http_error_code


class HelpIntentHandler(AbstractRequestHandler):
    """
    Class for Amazon's required HelpIntent.
    
    Arguments:
        AbstractRequestHandler {ask_sdk_core.dispatch_components.AbstractRequestHandler} -- Provided by Amazon's SDK.
    """

    def can_handle(self, handler_input):
        """
        Checks if intent can be executed.
        
        Arguments:
            handler_input {ask_sdk_core.handler_input.HandlerInput} -- Handler input provided by Amazon's SDK.
        
        Returns:
            [Boolean] -- True if user asked for help.
        """
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        """
        Checks if intent can be executed.
        
        Arguments:
            handler_input {ask_sdk_core.handler_input.HandlerInput} -- Provided by Amazon's SDK.
        
        Returns:
            [ask_sdk_model.response.Response] -- Response object (Amazon's SDK) with the appropiate response to the user.
        """
        i18n = LanguageModel(handler_input.request_envelope.request.locale)
        speech_text = i18n.HELP

        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """
    Class for Amazon's required StopIntent and CancelIntet
    
    Arguments:
        AbstractRequestHandler {ask_sdk_core.dispatch_components.AbstractRequestHandler} -- Provided by Amazon's SDK.
    
    """
    
    def can_handle(self, handler_input):
        """
        Checks if intent can be executed.
        
        Arguments:
            handler_input {ask_sdk_core.handler_input.HandlerInput} -- Provided by Amazon's SDK.
        
        Returns:
            [Boolean] -- True, if User stops or cancels.
        """
        
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        """
        Checks if intent can be executed.
        
        Arguments:
            handler_input {ask_sdk_core.handler_input.HandlerInput} -- Provided by Amazon's SDK.
        
        Returns:
            [ask_sdk_model.response.Response] -- Response object (Amazon's SDK) with the appropiate response to the user.
        """
        i18n = LanguageModel(handler_input.request_envelope.request.locale)
        speech_text = i18n.get_random_goodbye()

        handler_input.response_builder.speak(speech_text).set_should_end_session(True)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        sess_attrs = handler_input.attributes_manager.session_attributes
        i18n = LanguageModel(handler_input.request_envelope.request.locale)
        speech_text = i18n.FALLBACK_INTENT
        reprompt = i18n.FALLBACK_INTENT_REPROMPT

        handler_input.response_builder.speak(speech_text).ask(reprompt)
        sess_attrs.clear()

        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        return handler_input.response_builder.response


class CatchBackendExceptionHandler(AbstractExceptionHandler):
    """
    Exception handler for exceptions from the backend. Handler gets only executed if
    there is an exception in the skill.
    
    Arguments:
        AbstractExceptionHandler {ask_sdk_core.dispatch_components.AbstractExceptionHandler} -- Provided by Amazon's SDK.
    """
    def can_handle(self, handler_input, exception):
        """
        True if backend gives a HTTP error code.
        
        Arguments:
            handler_input {ask_sdk_core.handler_input.HandlerInput} -- Provided by Amazon's SDK.
            exception {[type]} -- [description]
        
        Returns:
            [Boolean] -- True, if server respons with HTTP error code.
        """
        sess_attrs = handler_input.attributes_manager.session_attributes

        if sess_attrs.get("HTTP_ERROR_CODE"):
            return True

    def handle(self, handler_input, exception):
        """
        Returns an appropriate response for HTTP error codes

        Arguments:
            handler_input {ask_sdk_core.handler_input.HandlerInput} -- Provided by Amazon's SDK
            exception {[type]} -- [description]
        
        Returns:
            [ask_sdk_model.response.Response] -- Response object with appropriate answer to user.
        """
        sess_attrs = handler_input.attributes_manager.session_attributes

        response = respond_to_http_error_code(handler_input, sess_attrs.get("HTTP_ERROR_CODE"))
        return response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """
    Exception handler class if no other handler gets executed.
    
    Arguments:
        AbstractExceptionHandler {ask_sdk_core.dispatch_components.AbstractExceptionHandler} -- Provided by Amazon's SDK.
    """
    def can_handle(self, handler_input, exception):
        """
        If no other handler gets exectued, this one handles the exception.

        Arguments:
            handler_input {ask_sdk_core.handler_input.HandlerInput} -- Provided by Amazon's SDK.
            exception {[type]} -- [description]
        
        Returns:
            [Boolean] -- Always True.
        """
        return True

    def handle(self, handler_input, exception):
        """
        If there is no intent handler that can handle the request, we got a detour exception.
        This happens in certain cases (user uses skill even though he is not authorized).
        Otherwise we just give a general error response.

        Arguments:
            handler_input {ask_sdk_core.handler_input.HandlerInput} -- Provided by Amazon's SDK.
            exception {[type]} -- [description]
        
        Returns:
            [ask_sdk_model.response.Response] -- Response object (Amazon's SDK)
        """
        print("Encountered following exception: {}".format(exception))
        sess_attrs = handler_input.attributes_manager.session_attributes
        i18n = LanguageModel(handler_input.request_envelope.request.locale)

        if "Couldn't find handler that can handle the request" in "{}".format(exception):
            detour_exception = True
        else:
            detour_exception = False

        if detour_exception and sess_attrs.get("ACCOUNT").get("AUTHORIZED"):
            speech = i18n.DETOUR_EXCEPTION
        elif detour_exception and not sess_attrs.get("ACCOUNT").get("AUTHORIZED"):
            speech = i18n.NOT_AUTHORIZED_DETOUR
        else:
            # Technically also backend exceptions will be logged here. E.G.: if problem when
            # sending a telegram. I don't catch all Backend exceptions, only on account
            # interceptor
            speech = i18n.FRONTEND_ERROR

        handler_input.response_builder.speak(speech).set_should_end_session(True)
        sess_attrs.clear()

        return handler_input.response_builder.response
