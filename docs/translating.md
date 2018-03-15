# Internationalization of EFLA-web

## Contents

- [Internationalization of EFLA-web](#internationalization-of-efla-web)
    - [Contents](#contents)
    - [1. Introduction](#1-introduction)
        - [1.1 Concepts](#11-concepts)
        - [1.2 Technologies used](#12-technologies-used)
        - [1.3 Location of files](#13-location-of-files)
        - [1.4 Language Identifiers](#14-language-identifiers)
    - [2. Workflows](#2-workflows)
        - [2.1 Changing the existing translation](#21-changing-the-existing-translation)
        - [2.2 Adding a new language](#22-adding-a-new-language)
        - [2.3 Changing the default language](#23-changing-the-default-language)
        - [2.4 Updating existing translation after a code change](#24-updating-existing-translation-after-a-code-change)
    - [3. Developers Guide](#3-developers-guide)
        - [3.1 Extending EFLA-web](#31-extending-efla-web)
            - [3.1.1 Immutable Strings](#311-immutable-strings)
                - [3.1.1.1 Example usage of `_()`](#3111-example-usage-of)
            - [3.1.2 Immutable String Identifiers](#312-immutable-string-identifiers)
                - [3.1.2.1 Example usage of `I18n()`](#3121-example-usage-of-i18n)
            - [3.1.3 Mutable Strings](#313-mutable-strings)
                - [3.1.3.1 Example Usage of `I15dString`](#3131-example-usage-of-i15dstring)
            - [3.1.4 When to use what](#314-when-to-use-what)
            - [3.1.5 Applying your changes](#315-applying-your-changes)
        - [3.2 Using the REST-like API](#32-using-the-rest-like-api)
            - [3.2.1 Specifying a locale](#321-specifying-a-locale)
            - [3.2.1.1 How locale is detected](#3211-how-locale-is-detected)
                - [3.2.1.2 In HTTP Headers](#3212-in-http-headers)
                - [3.2.1.3 As Request Parameter](#3213-as-request-parameter)
            - [3.2.2 The locale cookie](#322-the-locale-cookie)
            - [3.2.3 Format of internationalized strings](#323-format-of-internationalized-strings)


## 1. Introduction

The EFLA-web survey platform can be translated to any language supported by
_GNU gettext_. These translations concern the text displayed on EFLA-web pages,
messages displayed to DataClients when editing surveys, messages displayed to 
DataSubjects by the Questionnaire Access Control (QAC) and response messages
sent by the REST-like API.

### 1.1 Concepts

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

### 1.2 Technologies used

The internationalization of the platform is achieved with [_Babel_](http://babel.pocoo.org/en/latest/index.html).

### 1.3 Location of files

Translation related files are found in `EFLA-web/websrvs-flask/app/translations`.

All translated messages are defined in a template file, located at: 
`EFLA-web/websrv-flask/app/translations/messages.pot`

Translations of the strings are stored in 
`EFLA-web/websrv-flask/app/translations/<language shorthand>/LC_MESSAGES/meesages.po`

Translation files can be compiled into message catalogues, which are stored as
`EFLA-web/websrv-flask/app/translations/<language shorthand>/LC_MESSAGES/meesages.mo`

_<language shorthand>_ refers to a Language identifier.

### 1.4 Language Identifiers

All supported languages are listed in `/EFLA-web/websrv-flask/app/framework/internationalization/babel_languages.py`.

We generally refer to languages or locales by the lowercase two to three letter abbreviations defined there.

## 2. Workflows

### 2.1 Changing the existing translation

Just edit the `messages.po` of the language you want to change.

After editing the file, you need to compile it:

```bash
cd EFLA-web/websrv-flask/app
pybabel compile -d translations
```

You have to restart the stack for the changes to be applied, see _deployment.md_.

### 2.2 Adding a new language

If no `messages.po` file exists for a given language, it can be created by running:

```bash
cd EFLA-web/websrv-flask/app
pybabel init -i translations/messages.pot -d translations -l <language shorthand>
```

You can then edit and compile the `messages.po` file as described in 2.1.

### 2.3 Changing the default language

The default language or locale is defined in `EFLA-web/websrv-flask/app/flask.cfg` as `BABEL_DEFAULT_LOCALE` and can be set to any language identifier.

### 2.4 Updating existing translation after a code change

If a code change has happened (see 3.1 for a guide on how to do this) and new messages have been added or existing ones have been changed in the code, the message template file has to be updated:

```bash
cd EFLA-web/websrv-flask/app
pybabel extract -F babel.cfg -k I18n -o translations/messages.pot .
```

From the updated template file, you can the update the existing translation files by running:

```bash
cd EFLA-web/websrv-flask/app
pybabel update -i translations/messages.pot -d translations -l <language shorthand>
```

Existing translations will be kept and new messages will be added to the `messages.po` file.

You may then alter the translation file as described in 2.1. 

## 3. Developers Guide
### 3.1 Extending EFLA-web
#### 3.1.1 Immutable Strings

Immutable strings are strings that are hard coded into the source code and can't 
be changed by user interaction. For making immutable strings translatable, for
example when writing an error message or a text on a web page, the `_()`
function defined in `framework.internationalization` is used. The function maps
to `flask_babel.gettext` which fetches the appropriate translation of the
string at runtime.

##### 3.1.1.1 Example usage of `_()`

```python
def from_yaml(path_to_yaml: str):

    # we do something risky like opening a file
    with open(path_to_yaml) as fd:
        contents = yaml.load(fd)

    # and te need to communicate the error back
    if type(contents) != dict:
        raise Exception(_("Template needs to be a dictionary"))  # this will be translated on execution
            
```

#### 3.1.2 Immutable String Identifiers

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

##### 3.1.2.1 Example usage of `I18n()`

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

#### 3.1.3 Mutable Strings

Mutable strings are strings that can be changed at runtime by user interaction. 
An example for these are the Question texts in Questionnaires.

We modle these strings with the `I15dString` class, which is a database persistent `DataObject`.
As such they're identified by `I15dString.uuid`.

An `I15dString` contains a `default_locale` and a dictionary of `locales`.

```json
{
    "locales": {
        "de": "Ein text",
        "en": "A text",
        "eo": "HALLO HIER MICH GIBTS AUF ESPERANTO"
    },
    "default_locale": "en"
}
```

These locales are language identifiers as described in 1.4.

Use the `set_locale()` method to add a new translation to an instance of `I15dString`.

When serialized by `DataObjectEncoder`, all translations are serialized and it's the job
of the frontend to pick the right version to display.

##### 3.1.3.1 Example Usage of `I15dString`

```python

class Question(DataObject):

    @staticmethod
    def create_question(text: str) -> "Question":
        question = Question()
        question.text = I15dString.new(text)  # use .new() to initialize with text

        return question

    def set_text(text: str) -> None:
        self.text.set_locale(text)

    def get_text() -> str:
        self.text.get()

Question.text = DataPointer(Question, "text", I15dString, cascading_delete=True)
```

Note that the `cascading_delete` flag is set to True, meaning the `I15dString` instance
will be removed from the database when parent `Question` is removed (provided no other
instance of `DataObject` has a strong reference to it). This is generally a good idea
to prevent memory leaks.

When initializing an `I15dString` with `I15dString.new()` or setting the translation with
`I15dString.set_locale()` without a locale specified, the locale of the current request will be used.

Use `I15dString.get()` to return the strings representation in the currently requested locale. 
If no representation for the requested locale is found, the default locale will be returned. 

#### 3.1.4 When to use what

Use `_()` when:

- The content of the strings never changes
- writing Exception messages
- writing HTML templates
- writing API response messages
- you don't need to compare the string to anything 

Use `I18n()` when:

- The content of the strings never changes
- You need to compare the string to another

Use `I15dString` when:

- Persisting user input in the database

#### 3.1.5 Applying your changes 

See 2.4.

### 3.2 Using the REST-like API
#### 3.2.1 Specifying a locale

We try to always serve the right locale. When the requested locale is not found, the default
locale is used.

#### 3.2.1.1 How locale is detected

The request parameter overrides the cookie, which overrides the DataClient's account language, which overrides the HTTP header.

##### 3.2.1.2 In HTTP Headers

Set the `Accept-Language' filed in the HTTP header to the requested locale.

##### 3.2.1.3 As Request Parameter

Send `locale` as a request parameter with any request to request a specific locale.

#### 3.2.2 The locale cookie

The first time a client's locale is detected, we hand out a cookie with the detected locale.

This cookie will be used from this moment on. To be issued a new cookie, manually set the `locale` request
parameter to a different locale.

#### 3.2.3 Format of internationalized strings
    
```json
{   
    "class": "model.I15dString.I15dString",
    "uuid": "some_hexdigit_uuid",
    "locales": {
        "de": "Ein text",
        "en": "A text",
        "eo": "HALLO HIER MICH GIBTS AUF ESPERANTO"
    },
    "default_locale": "en"
}
```