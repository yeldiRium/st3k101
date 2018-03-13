import hashlib

from framework.odm.DataObject import DataObject
from framework.odm.DataAttribute import DataAttribute


class DataSubject(DataObject):
    has_owner = False

    @staticmethod
    def get_or_create(email_address):
        # hash email address of user to anonymize data
        email = email_address.encode("utf-8")
        hasher = hashlib.new('ripemd160')
        hasher.update(email)
        email_hashed = hasher.hexdigest()

        # get existing DataSubject or create new
        data_subject = DataSubject.one_from_query(
            {"email_hash": email_hashed})
        if data_subject is None:
            data_subject = DataSubject()
            data_subject.email = email_hashed

        return data_subject


DataSubject.confirmation_token = DataAttribute(DataSubject, "confirmation_token", serialize=False)
DataSubject.email_hash = DataAttribute(DataSubject, "email_hash")
