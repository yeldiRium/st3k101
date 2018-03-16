# Object Document Mapper

## Introduction

The ODM is a small database abstraction library which maps Python's object
lifecycle to records in mongodb.

It provides a declarative interface that allows you to define a database
model object-oriented-style in Python.

The declared classes can then by used like plain python, but actions on them
are transparently mapped to database actions.

The source can be found in `EFLA-web/websrv-flask/app/framework/odm`.

## Declarative Interface

### DataObject

The base class for everything else is DataObject. It represents a single record
in the database. It is identified uniquely by it's uuid.

A DataObject may have any number of Attributes which are stored in the database
and accessible through the python class. It may also have references to other
DataObjects.

### Definition

To define a new DataObject, simply inherit from the DataObject class.

#### Creation

When creating a DataObject, we may pass an uuid to retrieve a specific object
from the database.

If no uuid is passed, a new DataObject of the given class is created in the 
database.

#### Ownership

Any DataObject may be owned by a DataClient.

When trying to retrieve an object from the database that isn't owned by the 
currently logged in DataClient, and AccessControlException is raised.

When creating a new DataObject, the owner will be the currently logged in DataClient,
unless an owner is specifically passed with the constructor.

When a DataObject class should be readable by non-owner users but should not
be altered by them, you can set the `readable_by_anonymous=True` flag on the class:

```python
class Question(DataObject):
    readable_by_anonymous = False
```

If a DataObject is instantiated, but can't be written to, the `DataObject.readonly`
property will evaluate to `True`.

You may also deactivate access control completely for a class by setting
`has_owner=False`:

```python
class DataClient(DataObject):
    has_owner = False
```

#### Object-Level Locking

DataObjects are locked on an per-object basis when accessed. This means that at
any given time, only one thread may access a DataObject.

This locking behaviour is achieved through a shared mutex semaphore that is
stored in memcached.

When a thread tries to acquire an already locked DataObject, it will wait a
random time and retry. This ensures that every thread will sooner or later
be granted access.

Within a thread, DataObjects are singleton objects. When instantiating multiple
DataObjects with the same uuid, the same instance will be returned by the
constructor.

### DataAttribute

To make members of DataAttribute database persistent, define them as DataAttributes:

```python
class DataClient(DataObject):
    pass
    
DataClient.email = DataAttribute(DataClient, "email")
```

Everytime `DataClient.email` is accessed, it is either retrieved from the database
or written to the database.

DataAttribute supports all types that are JSON serializable.

### References to other DataObjects

Sometimes attributes are references to other DataObject. We support multiple
cardinality types.

References to other DataObjects are stored as uuids in the database, the 
appropriate DataObject class is instantiated when accessing a reference in python.

#### DataPointer

A 1 to 1 cardinality reference, which references exactly one or zero other
DataObjects.

Example:

```python
class QuestionResult(DataObject):
    pass

QuestionResult.data_subject = DataPointer(QuestionResult, "data_subject",
                                          DataSubject)
QuestionResult.answer_value = DataAttribute(QuestionResult, "answer_value")

new_subject = DataSubject()
new_result = QuestionResult()

new_result.data_subject = new_subject
new_result.answer_value = 3
```

#### DataPointerSet

A 1 to n cardinality reference, which references an unordered collection of
unique DataObjects of the same class.

DataPointerSet supports all standard actions on sets in python.

Example:

```python
class Questionaire(DataObject):
    pass

# declaring
Questionaire.questions = DataPointerSet(QuestionResult, "questions", Question)


new_questionnaire = Questionaire()
new_question = Question()

new_questionnaire.questions.add(new_question)  # adding

for q in new_questionnaire.questions:  # iterating
    print(q.text)
    
new_questionnaire.questions.remove(new_question)  # removing
```

#### MixedDataPointerSet

A 1 to n cardinality reference, which references an unordered collection of
unique DataObjects. The referenced DataObjects may have multiple classes.

MixedDataPointerSet supports all actions DataPointerSet supports.

There is a storage overhead for this type of reference as the DataObject class
has to be saved as well.

Use DataPointerSet if only referencing DataObjects of one class.

Example:

```python
class DataClient(DataObject):
    pass
    
DataClient.friends = MixedDataPointerSet(DataClient, "friends")

new_data_client = DataClient()
their_friend = DataClient()
their_other_friend = DataSubject()

new_data_client.friends.add(their_friend)
new_data_client.friends.add(their_other_friend)
```

#### Reference Counting

All reference types support reference counting.

Every DataObject has a reference count, which is the number of strong references
other DataObjects have to it.

References are `PointerType.WEAK` by default, but can be declared with 
`pointer_type=PointerType.STRONG` to make them strong references.

A strong reference to a DataObject will prevent it's deletion.

#### cascading_delete

All reference types support the `cascading_delete=True` flag. When this flag is
set, and a DataObject is deleted, all referenced DataObjects are also deleted,
provided no other strong reference points to them.

## JSON serialization

All DataObjects can be encoded by the DataObjectEncoder class. The encoder
will automatically recurse through all Attributes and Pointers to other
DataObject defined with the declarative interface.

### Access Control

When recursing through an object hierarchy, we might encounter a reference to
a DataObject we're not allowed to access, because we do not own it and it's
not `readable_by_anonymous`. In this case, the serialization of the non-accessible
object is skipped.

### serialize=False

Any Attribute and Pointer defined with the declarative interface may be created
with the `serialize=False` flag set. If this flag is set, the encoder will skip
this attribute when encoding.

Example:

```python
class DataClient(DataObject):
    has_owner = False

DataClient.email = DataAttribute(DataClient, "email")
DataClient.password_salt = DataAttribute(DataClient, "password_salt",
                                         serialize=False)
DataClient.password_hash = DataAttribute(DataClient, "password_hash",
                                         serialize=False)
```

### exposed_properties

A DataObject may define a number of additional properties that will be encoded
by the DataObjectEncoder.

Example:

```python
class DataClient(DataObject):
    has_owner = False
    exposed_properties = {
        "gravatar"
    }
    
    @property
    def gravatar(self) -> bytes:
        return get_gravatar(self.email)


DataClient.email = DataAttribute(DataClient, "email")
```

## Limitations

### Lack of Transaction Model

Apart from object-level locking, there is no transaction model which would
guarantee transaction atomicity for larger transactions.

This means when a request fails halfway through, it will only have written
half of the data. 

The lack of a more sophisticated transaction model is due to time constraints
and not wanting to write a scheduler.

### No Inheritance

The declarative interface doesnt yet support inheritance of DataAttributes or
DataPointers.

This means event though we can inherit logic from DataObjects, we have to redefine
common attributes in each inherited class.
