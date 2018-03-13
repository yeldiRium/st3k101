# Translating EFLA-web

## Introduction

The EFLA-web survey platform can be translated to any language supported by
_GNU gettext_. These translations concern the text displayed on EFLA-web pages,
messages displayed to DataClients when editing surveys, messages displayed to 
DataSubjects by the Questionnaire Access Control (QAC) and response messages
sent by the REST-like API.

Text messages that should be translated on runtime are marked with 
 
`_()` as in: `_("Some text message")` 

or 

`I18n()` as in: `I18n("Some text message")`

in the source code and in html templates.
The marked text messages are extracted with the help of _pybabel_.

_pybabel_ then creates translation files from the extracted message file.

A translator may then fill in the newly created translation file.

When a request is submitted to the EFLA-web platform, the requested locale
is automatically detected and we try to serve the requested translation for
all marked messages. When the requested locale is not found, the default locale
defined in `flask.cfg` is served.

## How to make your code translatable

In order to make the whole platform translatable to different languages, we
considered three cases:

### Constant strings

Constant strings are strings that are hard coded into the source code and can't 
be changed by user interaction. For making hard coded strings translatable, for
example when writing an error message or a text on a web page, the `_()`
function defined in `framework.internationalization` is used. The function maps
to `flask_babel.lazy_gettext` which fetches the appropriate translation of the
string at runtime, when the string is accessed (hence the `lazy_` prefix).

#### Example usage of `_()`

```python
def from_yaml(path_to_yaml: str):

    # we do something risky like opening a file
    with open(path_to_yaml) as fd:
        contents = yaml.load(fd)

    # and te need to communicate the error back
    if type(contents) != dict:
        raise Exception(_("Template needs to be a dictionary"))
            
```

### Database persistent strings

Sometimes, we use strings to identify things at runtime. We might for example
define an Enum containing different menu items and persist Enum items in the
database, for example to remember which menu items the user has chosen.
In this case, we can't use `_()` as this would mean that the translated string
would be written to the database, which makes it hard to compare to others.
Writing translated strings into the database would also mean losing
comparability when the translation is updated and new and old strings differ.

For this, we use the `I18n()` class. It contains a `.msgid` and a `.text`
property, where `msgid` is the string you initialize `I18n()` with in the source
code and doesn't change and `text` always returns the currently appropriate
translation of `msgid`.

To use `I18n()` (if you haven't read up on how to work with the ODM, this would
be a good time), add a `DataString` member to the definition of a `DataObject`.
The `DataString` member will return an `I18n` object when accessed and accept
`I18n` object when set.

#### Example usage of I18n()

```python
from framework.odm.DataString import I18n, DataString
from framework.odm.DataObject import DataObject

class SomeMenuItem(DataObject):

    @staticmethod
    def new() -> "MenuItem":
        """
        :return: A new instance of this, avec les defaults
        """

        # Set up new MenuItem instance
        the_new_item = SomeMenuItem()
        the_new_item.label = I18n("Some text!")
        the_new_item.description = I18n("""
                                        Some longer description text, for
                                        example for a mouse over help box.    
                                        """)

        return the_new_item


SomeMenuItem.label = DataString(SomeMenuItem, "label")
SomeMenuItem.description = DataString(SomeMenuItem, "description")
```

You can the access the object like this:

```python
some_menu_item = SomeMenuItem.new()
some_other_item = SomeMenuItem.new()

some_menu_item.label = I18n("Oops, my label changed :O")

# >>> some_menu_item.label == some_other_item.label
# False

# >>> some_menu_item.label.text
# Oh, mein Label hat sich verändert :O
```

### Dynamic strings


## Adding a new translation

All translated messages are defined in a template file, located at: 
`EFLA-web/websrv-flask/app/translations/messages.pot`

Translations of the strings are stored in 
`EFLA-web/websrv-flask/app/translations/<language shorthand>/LC_MESSAGES/meesages.po`

To add a new translation, run:

```bash
cd EFLA-web/websrv-flask/app
pybabel init -i translations/messages.pot -d translations -l <lanugae shorthand>
```

Where _\<language shorthand>_ is an abbreviation for the language, as defined
in `/EFLA-web/websrv-flask/app/framework/internationalization/babel_languages.py`.

You can then edit the `messages.po`. When done, run:

```bash
cd EFLA-web/websrv-flask/app
pybabel compile -d translations
```

Restart the EFLA-web stack.

## Updating a translation

Just edit the `messages.po`. Obtained from the step above and compile it via:

```bash
cd EFLA-web/websrv-flask/app
pybabel compile -d translations
```

## Updating translations after a code change

When new messages have been added to the code or some have been removed, the
message template file has to be updated. To do this, run:

```bash
cd EFLA-web/websrv-flask/app
pybabel extract -F babel.cfg -k I18n -o translations/messages.pot .
```

You can then update the 
