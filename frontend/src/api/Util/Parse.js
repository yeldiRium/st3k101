import {map, prop} from "ramda";

import {Language, LanguageData} from "../../model/Language";
import DataClient from "../../model/DataClient";
import {
    ConcreteQuestionnaire,
    ShadowQuestionnaire
} from "../../model/SurveyBase/Questionnaire";
import Resource from "../../model/Resource";

/**
 * Parses the API representation of a Language into a Language object.
 *
 * @param {String} item_id
 * @param {String} value
 * @return {Language}
 */
function parseLanguage({item_id, value}) {
    return new Language(item_id, value);
}

/**
 * Parses the three language components usually contained in any translatable
 * object in the API into a LanguageData object.
 *
 * @param current_language
 * @param original_language
 * @param available_languages
 * @return {LanguageData}
 */
function parseLanguageData({
                               current_language,
                               original_language,
                               available_languages
                           }) {
    return new LanguageData(
        parseLanguage(current_language),
        parseLanguage(original_language),
        map(parseLanguage, available_languages)
    );
}

/**
 * Parses the common API representation of a DataClient into a DataClient in-
 * stance.
 *
 * @param {String} email
 * @param {Number} id
 * @param {String} href
 * @param {Object} language
 * @return {DataClient}
 */
function parseDataClient({email, id, href, language}) {
    return new DataClient(
        href,
        id,
        email,
        parseLanguage(language)
    );
}

/**
 * Parses the common API representation of a Questionnaire and recognizes, whe-
 * ther it is a ShadowQuestionnaire or a ConcreteQuestionnaire.
 *
 * @param {Object} data
 * @return {Questionnaire}
 */
function parseQuestionnaire(data) {
    if (prop("shadow", data) === true) {
        return parseShadowQuestionnaire(data);
    }
    return parseConcreteQuestionnaire(data);
}

/**
 * Parses the common API representation of a ShadowQuestionnaire.
 *
 * @param {String} href
 * @param {String} id
 * @param {String} name
 * @param {String} description
 * @param {Array} dimensions
 * @param {Boolean} published
 * @param {Boolean} template
 * @param {Boolean} allow_embedded
 * @param {String} xapi_target
 * @param {Object} current_language
 * @param {Object} original_language
 * @param {Array} available_languages
 * @param {Array} qac_modules TODO: handle QAC modules
 *
 * @return {ShadowQuestionnaire}
 */
function parseShadowQuestionnaire({
                                      href,
                                      id,
                                      name,
                                      description,
                                      dimensions,
                                      published,
                                      template,
                                      allow_embedded,
                                      xapi_target,
                                      current_language,
                                      original_language,
                                      available_languages,
                                      qac_modules
                                  }) {
    return new ShadowQuestionnaire(
        href,
        id,
        new Resource("", ""), // TODO: set once API is adjusted to output Owner
        parseLanguageData({
            current_language,
            original_language,
            available_languages
        }),
        name,
        description,
        published,
        allow_embedded,
        xapi_target,
        map(parseDimension(dimensions)),
        null // TODO: set once API is adjusted to output referenceTo
    )
}

/**
 * Parses the common API representation of a ConcreteQuestionnaire.
 *
 * @param {String} href
 * @param {String} id
 * @param {String} name
 * @param {String} description
 * @param {Array} dimensions
 * @param {Boolean} published
 * @param {Boolean} template
 * @param {Boolean} allow_embedded
 * @param {String} xapi_target
 * @param {Object} current_language
 * @param {Object} original_language
 * @param {Array} available_languages
 * @param {Array} qac_modules TODO: handle QAC modules
 *
 * @return {ConcreteQuestionnaire}
 */
function parseConcreteQuestionnaire({
                                        href,
                                        id,
                                        name,
                                        description,
                                        dimensions,
                                        published,
                                        template,
                                        allow_embedded,
                                        xapi_target,
                                        current_language,
                                        original_language,
                                        available_languages,
                                        qac_modules
                                    }) {
    return new ConcreteQuestionnaire(
        href,
        id,
        new Resource("", ""), // TODO: set once API is adjusted to output Owner
        parseLanguageData({
            current_language,
            original_language,
            available_languages
        }),
        name,
        description,
        published,
        allow_embedded,
        xapi_target,
        map(parseDimension(dimensions)),
        0, // TODO: set once API is adjusted to output incomingReferenceCount
        [] // TODO: set once API is adjusted to output ownedIncomingReferences
    )
}

/**
 * Parses the common API representation of a Dimension and recognizes, whe-
 * ther it is a ShadowDimension or a ConcreteDimension.
 *
 * @param {Object} data
 * @return {Dimension}
 */
function parseDimension(data) {
    return {};
}

export {
    parseLanguage,
    parseLanguageData,
    parseDataClient,
    parseQuestionnaire,
    parseShadowQuestionnaire,
    parseConcreteQuestionnaire
};
