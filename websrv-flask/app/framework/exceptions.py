class ClientIpChangedException(Exception):
    pass


class ClassnameMismatchException(Exception):
    pass


class UuidMismatchException(Exception):
    pass


class ObjectDoesntExistException(Exception):
    pass


class BadCredentialsException(Exception):
    pass


class SessionExistsException(Exception):
    pass


class UserExistsException(Exception):
    pass


class UserNotLoggedInException(Exception):
    pass


class BadQueryException(Exception):
    pass


class QuestionGroupNotFoundException(Exception):
    pass


class QuestionNotFoundException(Exception):
    pass


class QuestionnaireNotFoundException(Exception):
    pass


class DuplicateQuestionnaireNameException(Exception):
    pass


class AccessControlException(Exception):
    pass


class QuestionStatisticHasNoQuestionException(Exception):
    pass


class DuplicateQuestionNameException(Exception):
    pass


class DuplicateSurveyNameException(Exception):
    pass


class LocaleNotFoundException(Exception):
    pass


class DuplicateQuestionGroupNameException(Exception):
    pass


class QACAlreadyEnabledException(Exception):
    pass


class QACNotEnabledException(Exception):
    pass


class YAMLTemplateInvalidException(Exception):
    pass