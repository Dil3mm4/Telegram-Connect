import random


class GenericLanguageModel(object):
    def __init__(self, locale):
        self.skill_name = "My Telegrams"

        self.BACKEND_EXCEPTION = None
        self.FRONTEND_ERROR = None
        self.SERVER_ERROR = None
        self.ACCOUNT_LINKING_REQUIRED = None
        self.WRONG_INTENT = None
        self.ACKS = None
        self.ACCEPTANCE_ACKS = None
        self.DONE_ACKS = None
        self.THINKING = None
        self.DONT_UNDERSTAND = None
        self.WELCOME = None
        self.FALLBACK = None
        self.FALLBACK_INTENT = None
        self.FALLBACK_INTENT_REPROMPT = None
        self.HELP = None
        self.GOODBYES = None
        self.ANYTHING_ELSE = None
        self.DETOUR_EXCEPTION = None

        self.BREAK_150 = "<break time='150ms'/>"
        self.BREAK_200 = "<break time='200ms'/>"

        if locale == "de-DE":
            self.set_generic_phrases_german()
        else:
            self.set_generic_phrases_english()

    def set_generic_phrases_german(self):
        self.ACKS = ["Okay", "In Ordnung", "Alles klar", "Okey Dokey"]
        self.ACCEPTANCE_ACKS = ["Okay", "In Ordnung", "Alles klar"]
        self.DONE_ACKS = ["Okay", "In Ordnung", "Alles klar", "Geschafft"]
        self.THINKING = ["Umm", "Ahhm", "Hmmm"]
        self.ANYTHING_ELSE = ["Gibt es sonst noch was?",
                              "Gibt es noch etwas wobei ich dir helfen kann?"
                              "Brauchst du noch etwas?", "Noch etwas?"]
        self.GOODBYES = ["adiós", "aloha", "arrivederci", "ciao", "auf Wiedersehen", "au revoir",
                         "bon voyage", "shalom", "vale"]
        self.DONT_UNDERSTAND = ["Sorry", "Entschuldigung", "Pardon"]

        self.BACKEND_EXCEPTION = "Das ist ein Fehler, der nicht passieren dürfte. Tut mir leid."
        self.FRONTEND_ERROR = self.get_random_thinking() + ", es ist ein Fehler aufgetreten. Versuche es später noch einmal. " + self.get_random_goodbye()
        self.SERVER_ERROR = "Aufgrund von Server Updates ist dieser Skill momentan nicht " \
                            "verfügbar. Versuche es später erneut "
        self.ACCOUNT_LINKING_REQUIRED = "Du benötigst einen {} Account um diesen Skill " \
                                        "nutzen zu können. Bevor du diesen Skill verwenden kannst, benutze die Alexa app um deinen " \
                                        "Amazon Account mit dem {} Account" \
                                        " zu verknüpfen.".format(self.skill_name, self.skill_name)

        self.WRONG_INTENT = "Sorry das habe ich jetzt nicht nachvollziehen können. Ich kann dir " \
                            "hier nicht weiter helfen. "
        self.DETOUR_EXCEPTION = "Sorry, " + self.skill_name + " kann dir hier nicht weiterhelfen. Ein mögliches Problem ist, dass du mit: 'Ja' auf ein Telegram antworten möchtest. Das ist nicht möglich. " + self.get_random_goodbye()

        ##############################
        # Required intents
        ##############################
        self.WELCOME = "Willkommen"
        self.FALLBACK = self.get_random_dont_understand() + ", was hast du gesagt?"
        self.FALLBACK_INTENT = "{} kann dir dabei nicht helfen. Du kannst entweder ein Telegram " \
                               "verschicken oder checken ob es neue gibt. Also, was brauchst " \
                               "du?".format(self.skill_name)
        self.FALLBACK_INTENT_REPROMPT = self.get_random_thinking() + ", ich habe das nicht " \
                                                                     "verstanden. Sage entweder: " \
                                                                     "'Versende ein Telegram' " \
                                                                     "oder 'Checke meine " \
                                                                     "Telegramme' "
        self.HELP = "{} verbindet Alexa mit deinem Telegram Messenger. Du kannst ein Telegram zu " \
                    "einer Person, Gruppe oder einem Bot schicken. Alternativ kannst du, " \
                    "falls ich Probleme habe den Namen zu verstehen, ein 'Speedgram' verschicken. " \
                    "Außerdem kannst du checken ob du neue Telegrame hast. Sage:  'Verschicke ein " \
                    "Telegram.' oder 'Checke meine Telegramme.' oder 'Verschicke ein " \
                    "Speedgram.'".format(self.skill_name)

    def set_generic_phrases_english(self):
        self.ACKS = ["Okay", "Alright", "Okey Dokey"]
        self.ACCEPTANCE_ACKS = ["Okay", "Sure", "Alright", "Got it", "You got it"]
        self.DONE_ACKS = ["Okay", "Alright", "Got it", "Done", "You got it"]
        self.THINKING = ["Umm", "Ahhm", "Hmmm"]
        self.ANYTHING_ELSE = ["Anything else?", "Is there something else I can help you with?",
                              "Do you need anything else?", "Is there something else you need?"]
        self.DONT_UNDERSTAND = ["Sorry", "Excuse me", "Pardon"]
        self.GOODBYES = ["adiós", "aloha", "arrivederci", "ciao", "auf Wiedersehen", "au revoir",
                         "bon voyage", "shalom", "vale"]

        self.BACKEND_EXCEPTION = "This is an error that shouldn't happen. I am sorry."
        self.FRONTEND_ERROR = self.get_random_thinking() + ", an unexpected error happened. Try again later. " + self.get_random_goodbye()
        self.SERVER_ERROR = "Due to updates the service is currently not available." \
                            " Try again later."
        self.ACCOUNT_LINKING_REQUIRED = "Welcome to {}. {} let's you connect Alexa with your Telegram Messenger. " \
                                        "You must have a {} account to use this skill." \
                                        " Go to the Alexa app to link " \
                                        "your Amazon account with your {} Account. Visit the website" \
                                        " mentioned in the skill description. " \
                                        "Bye for now.".format(self.skill_name, self.skill_name,
                                                              self.skill_name, self.skill_name)

        self.WRONG_INTENT = "I didn't quite catch that. I can't help you here."

        ##############################
        # Required intents
        ##############################
        self.WELCOME = "Welcome"
        self.FALLBACK = self.get_random_dont_understand() + ", what did you say?"
        self.FALLBACK_INTENT = "{} can't help you here. You can either send a Telegram or check " \
                               "for new ones. So, which do you need?".format(self.skill_name)
        self.FALLBACK_INTENT_REPROMPT = self.get_random_thinking() + ", I am still having trouble " \
                                                                     "understanding you. You can " \
                                                                     "either say: 'Send a " \
                                                                     "telegram' or 'Check my " \
                                                                     "Telegrams' "
        self.HELP = "{} connects Alexa with your Telegram Messenger. You can send a Telegram to a " \
                    "person, group, or bot. Alternately, If I have trouble understanding a " \
                    "complex name, you can use the speed dial feature to send a telegram. " \
                    "Furthermore, you can also check for new telegrams. Say: 'Check my " \
                    "telegrams.' or 'Send a telegram' or " \
                    "'send a speedgram' ".format(self.skill_name)
        self.DETOUR_EXCEPTION = "Sorry, " + self.skill_name + " can't help you here. A possible problem is that you wanted to reply with: 'Yes' to a Telegram. That is not possible. Bye for now"

    def get_random_ack(self):
        return random.choice(self.ACKS)

    def get_random_acceptance_ack(self):
        return random.choice(self.ACCEPTANCE_ACKS)

    def get_random_done_ack(self):
        return random.choice(self.DONE_ACKS)

    def get_random_goodbye(self):
        return random.choice(self.GOODBYES)

    def get_random_thinking(self):
        return random.choice(self.THINKING)

    def get_random_anyting_else(self):
        random_anyting_else = random.choice(self.ANYTHING_ELSE)
        return self.get_random_done_ack() + ". " + random_anyting_else

    def get_random_anyting_else_without_ack(self):
        return random.choice(self.ANYTHING_ELSE)

    def get_random_dont_understand(self):
        return random.choice(self.DONT_UNDERSTAND)