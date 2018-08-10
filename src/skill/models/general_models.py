class DailyTelegramsAccount(object):
    def __init__(self, id, phone_number, authorized):
        self.id = id
        self.phone_number = phone_number
        self.is_authorized = authorized


class Contact(object):
    def __init__(self, first_name, speed_dial_number=None, last_name=None, telegram_id=None):
        self.first_name = first_name
        self.speed_dial_number = speed_dial_number
        self.last_name = last_name
        self.telegram_id = telegram_id


class Conversation(object):
    def __init__(self, sender, telegrams, is_group, entity_id):
        self.sender = sender
        self.telegrams = telegrams
        self.is_group = is_group
        self.entity_id = entity_id
