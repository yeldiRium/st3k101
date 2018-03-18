from framework.odm.DataObject import DataObject
from framework.odm.DataString import DataString


class QACParameter(DataObject):
    """
    Abstract superclass for QACParameters.
    Never actually used, just for type hinting support and setting
    readable_by_anonymous for subclasses.
    
    QACParameters are user editable preferences for QACModules.
    
    QACModules enumerate their QACParameters. When accessed by the API,
    the QACModule serializes its QACModule.parameters, the 
    api_qac_configure endpoint can be used to modify a QACModule's QACParameter
    values.
    
    There are different QACParameter subclasses which represent different types
    of HTML input elements and can be rendered by the frontend automatically:
    
        - QACTextParameter:     An HTML text input
        - QACCheckboxParameter: An HTML checkbox input
        - QACSelectParameter:   An HTML select input
        - QACI15dTextParameter: An HTML text input with multiple representations
                                in different languages
    
    Each QACParameter has a name and a description which is displayed to the
    DataClient when adjusting the QACModule preferences.
    """
    readable_by_anonymous = True


QACParameter.name = DataString(QACParameter, "name")
QACParameter.description = DataString(QACParameter, "description")