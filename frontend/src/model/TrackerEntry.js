/**
 * TrackerEntry model, base class for tracker entries
 */
class TrackerEntry {
    /**
     *
     * @param {String} dataclientEmail
     * @param {Date} timestamp
     */
    constructor(dataclientEmail,
                timestamp
    ) {
        this._dataclientEmail =  dataclientEmail;
        this._timestamp = timestamp;
    }

    /***
     * @returns {String|*}
     */
    get dataclientEmail() {
        return this._dataclientEmail;
    }

    /**
     *
     * @returns {Date|*}
     */
    get timestamp() {
        return this._timestamp;
    }
}

/***
 * TrackerEntry that indicates that a property of a SurveyBase item
 * changed.
 */
class PropertyUpdatedTrackerEntry extends TrackerEntry {
    /**
     *
     * @param dataclientEmail {String}
     * @param timestamp {Date}
     * @param itemName {String}
     * @param itemType {String}
     * @param itemHref {String}
     * @param propertyName {String}
     * @param previousValue {*}
     * @param newValue {*}
     */
    constructor(dataclientEmail,
                timestamp,
                itemName,
                itemType,
                itemHref,
                propertyName,
                previousValue,
                newValue
    ) {
        super(dataclientEmail, timestamp);
        this._item = {
            name: itemName,
            type: itemType,
            href: itemHref
        };
        this._propertyName = propertyName;
        this._previousValue = previousValue;
        this._newValue = newValue;
    }

    get itemName() {
        return this._item.name;
    }

    get itemType() {
        return this._item.type;
    }

    get itemHref() {
        return this._item.href;
    }

    get propertyName() {
        return this._propertyName;
    }

    get previousValue() {
        return this._previousValue;
    }

    get newValue() {
        return this._newValue;
    }
}

/**
 * TrackerEntry that indicates that a translation of a property
 * was changed.
 */
class TranslatedPropertyUpdatedTrackerEntry
    extends PropertyUpdatedTrackerEntry {
    /**
     *
     * @param dataclientEmail {String}
     * @param timestamp {Date}
     * @param itemName {String}
     * @param itemType {String}
     * @param itemHref {String}
     * @param propertyName {String}
     * @param previousValue {*}
     * @param newValue {*}
     * @param language {Language}
     */
    constructor(dataclientEmail,
                timestamp,
                itemName,
                itemType,
                itemHref,
                propertyName,
                previousValue,
                newValue,
                language
    ) {
        super(
            dataclientEmail,
            timestamp,
            itemName,
            itemType,
            itemHref,
            propertyName,
            previousValue,
            newValue
            );
        this._language = language;
    }

    get language() {
        return this._language;
    }
}

/**
 * TrackeEntry that indicates that a new SurveyBase item was added
 * to another.
 */
class ItemAddedTrackerEntry extends  TrackerEntry {
    constructor(dataclientEmail,
                timestamp,
                parentItemName,
                parentItemType,
                parentItemHref,
                addedItemName,
                addedItemType,
                addedItemHref
    ){
        super(dataclientEmail, timestamp);
        this._parentItem = {
            name: parentItemName,
            type: parentItemType,
            href: parentItemHref
        };
        this._addedItem = {
            name: addedItemName,
            type: addedItemType,
            href: addedItemHref
        };
    }

    get parentItemName() {
        return this._parentItem.name;
    }

    get parentItemType() {
        return this._parentItem.type;
    }

    get parentItemHref() {
        return this._parentItem.href;
    }

    get addedItemName() {
        return this._addedItem.name;
    }

    get addedItemType() {
        return this._addedItem.type;
    }

    get addedItemHref() {
        return this._addedItem.href;
    }
}

class ItemRemovedTrackerEntry extends TrackerEntry {
    constructor(dataclientEmail,
                timestamp,
                parentItemName,
                parentItemType,
                parentItemHref,
                removedItemName
    ) {
        super(dataclientEmail, timestamp);
        this._parentItem = {
            name: parentItemName,
            type: parentItemType,
            href: parentItemHref
        };
        this._removedItemName = removedItemName;
    }

    get parentItemName() {
        return this._parentItem.name;
    }

    get parentItemType() {
        return this._parentItem.type;
    }

    get parentItemHref() {
        return this._parentItem.href;
    }

    get removedItemName() {
        return this._removedItemName;
    }
}

class QuestionnaireRemovedTrackerEntry extends TrackerEntry {
    constructor(dataclientEmail,
                timestamp,
                questionnaireName
    ) {
        super(dataclientEmail, timestamp);
        this._questionnaireName = questionnaireName
    }

    get questionnaireName() {
        return this._questionnaireName;
    }
}

export {
    TrackerEntry,
    PropertyUpdatedTrackerEntry,
    TranslatedPropertyUpdatedTrackerEntry,
    ItemAddedTrackerEntry,
    ItemRemovedTrackerEntry,
    QuestionnaireRemovedTrackerEntry
}
