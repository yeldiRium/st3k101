class ClientIpChangedException(Exception): pass


class ClassnameMismatchException(Exception): pass


class UuidMismatchException(Exception): pass


class ObjectDoesntExistException(Exception): pass


class BadCredentialsException(Exception): pass


class SessionExistsException(Exception): pass


class UserExistsException(Exception): pass


class UserNotLoggedInException(Exception): pass


class BadQueryException(Exception): pass


class QuestionGroupNotFoundException(Exception): pass


class QuestionNotFoundException(Exception): pass


class QuestionnaireNotFoundException(Exception): pass


class DuplicateQuestionnaireNameException(Exception): pass


class AccessControlException(Exception): pass
