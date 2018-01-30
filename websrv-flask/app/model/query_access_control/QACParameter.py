from framework.odm.DataObject import DataObject
from framework.odm.DataPointer import DataPointer
from model.I15dString import I15dString


class QACParameter(DataObject):

    exposed_properties = {
        "label",
        "description"
    }

    @property
    def label(self):
        return self.i15d_label.get()

    @property
    def description(self):
        return self.i15d_description.get()


QACParameter.i15d_label = DataPointer(QACParameter, "i5d_label", I15dString,
                                      serialize=False)
QACParameter.i15d_description = DataPointer(QACParameter, "i15d_description",
                                            I15dString, serialize=False)
