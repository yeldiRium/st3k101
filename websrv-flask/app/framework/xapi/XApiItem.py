from abc import abstractmethod
import json


class XApiItem(object):
    """
    Represents a part of an xAPI statement e.g.
    an Actor or Verb.
    """

    @abstractmethod
    def as_dict(self):
        """
        Returns the xAPI item as dictionary.
        """
        raise NotImplementedError
    
    def as_json(self):
        """
        Returns the xAPI item in JSON format.
        """
        return json.dumps(self.as_dict())
