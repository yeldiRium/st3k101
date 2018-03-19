import hashlib

from framework.odm.DataObject import DataObject
from framework.odm.DataAttribute import DataAttribute

__author__ = "Noah Hummel, Hannes Leutloff"


class DataSubject(DataObject):
    """
    A DataObject representing a DataSubject.
    DataSubjects submit answers to Questionnaires.
    """
    has_owner = False

    @staticmethod
    def get_or_create(email_address: str) -> "DataSubject":
        """
        Factory method for getting an existing DataSubject from the database or
        returning an already existing DataSubject.
        :param email_address: str The email address of the DataSubject
        :return: DataSubject The newly created or already existing DataSubject
        """

        # hash email address of user to anonymize data
        email = email_address.encode("utf-8")
        hasher = hashlib.new('ripemd160')
        hasher.update(email)
        email_hash = hasher.hexdigest()

        # get existing DataSubject or create new
        data_subject = DataSubject.one_from_query(
            {"email_hash": email_hash})
        if data_subject is None:
            data_subject = DataSubject()
            data_subject.email_hash = email_hash

        return data_subject


DataSubject.confirmation_token = DataAttribute(DataSubject, "confirmation_token", serialize=False)
DataSubject.email_hash = DataAttribute(DataSubject, "email_hash")
