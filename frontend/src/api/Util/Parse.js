import {map, prop} from "ramda";

import {Language, LanguageData} from "../../model/Language";
import DataClient from "../../model/DataClient";
import Range from "../../model/SurveyBase/Config/Range";
import {
    ConcreteQuestionnaire,
    ShadowQuestionnaire
} from "../../model/SurveyBase/Questionnaire";
import {
    ConcreteDimension,
    ShadowDimension
} from "../../model/SurveyBase/Dimension";
import {
    ConcreteQuestion,
    ShadowQuestion
} from "../../model/SurveyBase/Question";
import {Resource} from "../../model/Resource";

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
 * Parses a simple resource.
 *
 * @param {String} href
 * @param {String} id
 * @returns {Resource}
 */
function parseResource({href, id}) {
    return new Resource(href, id);
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
 * Parses the anonymized API representation of a DataClient.
 *
 * @param id
 * @param href
 * @return {DataClient}
 */
function parseSmallDataClient({id, href}) {
    return new DataClient(
        href,
        id,
        "",
        null
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
 * @param {Array} owners
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
 * @param {Object} reference_to
 *
 * @return {ShadowQuestionnaire}
 */
function parseShadowQuestionnaire({
                                      href,
                                      id,
                                      owners,
                                      name,
                                      description,
                                      dimensions,
                                      published,
                                      allow_embedded,
                                      xapi_target,
                                      current_language,
                                      original_language,
                                      available_languages,
                                      qac_modules,
                                      reference_to
                                  }) {
    return new ShadowQuestionnaire(
        href,
        id,
        map(parseSmallDataClient, owners),
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
        map(parseDimension, dimensions),
        parseResource(reference_to)
    );
}

/**
 * Parses the common API representation of a ConcreteQuestionnaire.
 *
 * @param {String} href
 * @param {String} id
 * @param {Array} owners
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
 * @param {Array} owned_incoming_references
 * @param {Number} incoming_reference_count
 *
 * @return {ConcreteQuestionnaire}
 */
function parseConcreteQuestionnaire({
                                        href,
                                        id,
                                        owners,
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
                                        qac_modules,
                                        owned_incoming_references,
                                        incoming_reference_count
                                    }) {
    return new ConcreteQuestionnaire(
        href,
        id,
        map(parseSmallDataClient, owners),
        parseLanguageData({
            current_language,
            original_language,
            available_languages
        }),
        template,
        name,
        description,
        published,
        allow_embedded,
        xapi_target,
        map(parseDimension, dimensions),
        incoming_reference_count,
        map(parseResource, owned_incoming_references)
    );
}

/**
 * Parses the common API representation of a Dimension and recognizes, whe-
 * ther it is a ShadowDimension or a ConcreteDimension.
 *
 * @param {Object} data
 * @return {Dimension}
 */
function parseDimension(data) {
    if (prop("shadow", data) === true) {
        return parseShadowDimension(data);
    }
    return parseConcreteDimension(data);
}

/**
 * Parses the common API representation of a ShadowDimension.
 *
 * @param {String} href
 * @param {String} id
 * @param {Array} owners
 * @param {String} name
 * @param {Array} questions
 * @param {Boolean} randomize_question_order
 * @param {Boolean} template
 * @param {Object} current_language
 * @param {Object} original_language
 * @param {Array} available_languages
 * @param {Object} reference_to
 *
 * @return {ShadowDimension}
 */
function parseShadowDimension({
                                  href,
                                  id,
                                  owners,
                                  name,
                                  questions,
                                  randomize_question_order,
                                  current_language,
                                  original_language,
                                  available_languages,
                                  reference_to
                              }) {
    return new ShadowDimension(
        href,
        id,
        map(parseSmallDataClient, owners),
        parseLanguageData({
            current_language,
            original_language,
            available_languages
        }),
        name,
        map(parseQuestion, questions),
        randomize_question_order,
        parseResource(reference_to)
    );
}

/**
 * Parses the common API representation of a ConcreteQuestionnaire.
 *
 * @param {String} href
 * @param {String} id
 * @param {Array} owners
 * @param {String} name
 * @param {Array} questions
 * @param {Boolean} randomize_question_order
 * @param {Boolean} template
 * @param {Object} current_language
 * @param {Object} original_language
 * @param {Array} available_languages
 * @param {Array} owned_incoming_references
 * @param {Number} incoming_reference_count
 *
 * @return {ConcreteDimension}
 */
function parseConcreteDimension({
                                    href,
                                    id,
                                    owners,
                                    name,
                                    questions,
                                    randomize_question_order,
                                    template,
                                    current_language,
                                    original_language,
                                    available_languages,
                                    owned_incoming_references,
                                    incoming_reference_count
                                }) {
    return new ConcreteDimension(
        href,
        id,
        map(parseSmallDataClient, owners),
        parseLanguageData({
            current_language,
            original_language,
            available_languages
        }),
        template,
        name,
        map(parseQuestion, questions),
        randomize_question_order,
        incoming_reference_count,
        map(parseResource, owned_incoming_references)
    );
}

/**
 * Parses the common API representation of a Question and recognizes, whe-
 * ther it is a ShadowQuestion or a ConcreteQuestion.
 *
 * @param {Object} data
 * @return {Question}
 */
function parseQuestion(data) {
    if (prop("shadow", data) === true) {
        return parseShadowQuestion(data);
    }
    return parseConcreteQuestion(data);
}

/**
 * Parses the common API representation of a ShadowQuestion.
 *
 * @param {String} href
 * @param {String} id
 * @param {Array} owners
 * @param {String} text
 * @param {Number} range_start
 * @param {Number} range_end
 * @param {Boolean} template
 * @param {Object} current_language
 * @param {Object} original_language
 * @param {Array} available_languages
 * @param {Object} reference_to
 *
 * @return {ShadowQuestion}
 */
function parseShadowQuestion({
                                 href,
                                 id,
                                 owners,
                                 text,
                                 range_start,
                                 range_end,
                                 current_language,
                                 original_language,
                                 available_languages,
                                 reference_to
                             }) {
    return new ShadowQuestion(
        href,
        id,
        map(parseSmallDataClient, owners),
        parseLanguageData({
            current_language,
            original_language,
            available_languages
        }),
        text,
        new Range({start: range_start, end: range_end}),
        parseResource(reference_to)
    );
}

/**
 * Parses the common API representation of a ConcreteQuestionnaire.
 *
 * @param {String} href
 * @param {String} id
 * @param {Array} owners
 * @param {String} text
 * @param {Number} range_start
 * @param {Number} range_end
 * @param {Boolean} template
 * @param {Object} current_language
 * @param {Object} original_language
 * @param {Array} available_languages
 * @param {Array} owned_incoming_references
 * @param {Number} incoming_reference_count
 *
 * @return {ConcreteQuestion}
 */
function parseConcreteQuestion({
                                   href,
                                   id,
                                   owners,
                                   text,
                                   range_start,
                                   range_end,
                                   template,
                                   current_language,
                                   original_language,
                                   available_languages,
                                        owned_incoming_references,
                                        incoming_reference_count
                               }) {
    return new ConcreteQuestion(
        href,
        id,
        map(parseSmallDataClient, owners),
        parseLanguageData({
            current_language,
            original_language,
            available_languages
        }),
        template,
        text,
        new Range({start: range_start, end: range_end}),
        incoming_reference_count,
        map(parseResource, owned_incoming_references)
    );
}

export {
    parseLanguage,
    parseLanguageData,
    parseDataClient,
    parseQuestionnaire,
    parseShadowQuestionnaire,
    parseConcreteQuestionnaire,
    parseDimension,
    parseShadowDimension,
    parseConcreteDimension,
    parseQuestion,
    parseShadowQuestion,
    parseConcreteQuestion
};
