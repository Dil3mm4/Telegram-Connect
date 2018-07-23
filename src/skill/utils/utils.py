from difflib import SequenceMatcher
from html.parser import HTMLParser

from ask_sdk_model import Intent
from ask_sdk_model.dialog import ElicitSlotDirective
from six import PY3

############## PARSER ##############
from src.skill.i18n.language_model import LanguageModel
from src.skill.services.telethon_service import TelethonService


def convert_speech_to_text(ssml_speech):
    # convert ssml speech to text, by removing html tags
    s = SSMLStripper()
    s.feed(ssml_speech)
    return s.get_data()


class SSMLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.full_str_list = []
        if PY3:
            self.strict = False
            self.convert_charrefs = True

    def handle_data(self, d):
        self.full_str_list.append(d)

    def get_data(self):
        return ''.join(self.full_str_list)


############## CONTACT SEARCH / COMPARER ##############
def get_most_likely_name(first_names, slot_value):
    prev_percentage = 0
    s = StringComparer()
    contact = None

    for index, name in enumerate(first_names):
        percentage = s.similar(name, slot_value)
        if percentage > 0.7 and percentage > prev_percentage:
            prev_percentage = percentage
            contact = first_names[index]
    return contact


class StringComparer():
    def similar(self, a, b):
        # Lets make uppercase here, for better ratios
        a = a.upper()
        b = b.upper()
        return SequenceMatcher(None, a, b).ratio()


def send_telegram(first_name):
    print("SEND_TELEGRAM CONTACT")
    print(first_name)
    pass


def handle_authorization(handler_input):
    i18n = LanguageModel(handler_input.request_envelope.request.locale)
    telethon_service = TelethonService()
    sess_attrs = handler_input.attributes_manager.session_attributes
    account = sess_attrs.get("ACCOUNT")
    should_end = True
    slots = handler_input.request_envelope.request.intent.slots

    if not account.get("PHONE_NUMBER"):
        speech_text = "You have not added a telephone number. Visit the website mentioned in the skill description and add a telephone number then try again. Bye for now"
    elif not slots.get("code").value:
        telethon_service.send_code_request()

        updated_intent = Intent("CustomYesIntent", slots)
        elicit_directive = ElicitSlotDirective(updated_intent, "code")
        handler_input.response_builder.add_directive(elicit_directive)

        speech_text = "You received a code on your phone. <break time='200ms' /> What is the code?"
        should_end = False
    else:
        ok = telethon_service.sign_user_in(slots.get("code").value)

        if ok:
            sess_attrs["ACCOUNT"]["AUTHORIZED"] = True
            speech_text = "Done. You are now authorized. <break time='200ms'/> I can help you send a Telegram or check for new Telegrams. So, which do you need?"
            should_end = False
        else:
            speech_text = "The code is wrong. Please try again. Bye for now"

    handler_input.response_builder.speak(speech_text).set_should_end_session(should_end)
    return handler_input


class BackendException(Exception):
    def __init__(self, message):
        super(BackendException, self).__init__(message)