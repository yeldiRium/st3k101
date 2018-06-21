import Future from "fluture";
import {contains, without} from "ramda";

import {
    ConcreteQuestionnaire,
    ShadowQuestionnaire
} from "../model/SurveyBase/Questionnaire";
import {
    ConcreteDimension,
    ShadowDimension
} from "../model/SurveyBase/Dimension";
import {reloadDimension} from "./Dimension";
import {LanguageData} from "../model/Language";

/**
 * Create a new ConcreteQuestionnaire.
 *
 * @param {DataClient} owner
 * @param {Language} language
 * @param {String} name
 * @param {String} description
 * @param {Boolean} isPublic
 * @param {Boolean} allowEmbedded
 * @param {String} xapiTarget
 * @return {Future}
 * @resolve {ConcreteQuestionnaire}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function createConcreteQuestionnaire(owner,
                                     language,
                                     name,
                                     description,
                                     isPublic,
                                     allowEmbedded,
                                     xapiTarget = "") {
    // TODO: create via API
    // TODO: retrieve correct href
    const href = "";
    // TODO: retrieve correct id
    const id = "";
    const languageData = new LanguageData(language, language, [language]);

    // TODO: remove timeout. this is for testing purposes
    return Future((reject, resolve) => {
        window.setTimeout(resolve, 1500)
    }).chain(() => Future.of(new ConcreteQuestionnaire(
        href,
        id,
        owner,
        languageData,
        name,
        description,
        isPublic,
        allowEmbedded,
        xapiTarget,
        [],
        0,
        []
    )));
}

/**
 * Creates a new ShadowQuestionnaire based on the given ConcreteQuestionnaire.
 *
 * @param {DataClient} owner
 * @param {ConcreteQuestionnaire} questionnaire
 * @return {Future}
 * @resolve {ShadowQuestionnaire}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function createShadowQuestionnaire(owner, questionnaire) {
    // TODO: create via API
    // TODO: retrieve correct href
    const href = "";
    // TODO: retrieve correct id
    const id = "";
    const languageData = new LanguageData(
        questionnaire.languageData.currentLanguage,
        questionnaire.languageData.originalLanguage,
        [...questionnaire.languageData.availableLanguages]
    );
    // TODO: retrieve correct ShadowDimensions
    const shadowDimensions = [];

    reloadQuestionnaire(questionnaire);

    return Future.of(new ShadowQuestionnaire(
        href,
        id,
        owner,
        languageData,
        questionnaire.name,
        questionnaire.description,
        questionnaire.isPublic,
        questionnaire.allowEmbedded,
        questionnaire.xapiTarget,
        shadowDimensions,
        questionnaire
    ));
}

/**
 * Fetches a Questionnaire by a given href in the given language.
 *
 * @param {String} href
 * @param {Language} language
 *
 * @return {Future}
 * @resolve {Questionnaire}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function fetchQuestionnaire(href, language) {
    // TODO: fetch Questionnaire from API
    return Future.reject("Please implement this.");
}

/**
 * Reload the Questionnaire's data in its current language.
 *
 * @param {Questionnaire} questionnaire
 * @return {Future}
 * @resolve to true
 * @reject {TypeError|ApiError}
 * @cancel
 */
function reloadQuestionnaire(questionnaire) {
    // TODO: reload from API
    return Future.reject("Please implement this.");
}

/**
 * Delete the Questionnaire and all appended Dimensions.
 *
 * @param {Questionnaire} questionnaire
 * @return {Future}
 * @resolve {Boolean} with true
 * @reject {TypeError|ApiError}
 * @cancel
 */
function deleteQuestionnaire(questionnaire) {
    // TODO: delete via API
    return Future.reject("Please implement this.");
}

/**
 * Fetches the Questionnaire from the API in the requested language.
 *
 * @param {Questionnaire} questionnaire
 * @param {Language} language
 * @return {Future}
 * @resolve {Questionnaire}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function fetchTranslation(questionnaire, language) {
    // TODO: fetch translation from api
    // TODO: set languageData in questionnaire
    // TODO: set translated fields in questionnaire
    return Future.reject("Please implement this.");
}

/**
 * Sets the ConcreteQuestionnaire's name in the given language.
 *
 * @param {ConcreteQuestionnaire} questionnaire
 * @param {Language} language
 * @param {String} name
 * @return {Future}
 * @resolve to true
 * @reject {TypeError|ApiError}
 * @cancel
 */
function setName(questionnaire, language, name) {
    if (questionnaire.languageData.currentLanguage.equals(language)) {
        questionnaire.name = name;
    }

    // Error after setting name so that the app can be demonstrated without API.
    // TODO: set name via api in given language
    return Future.reject("Please implement this.");
}

/**
 * Sets the ConcreteQuestionnaire's description in the given language.
 *
 * @param {ConcreteQuestionnaire} questionnaire
 * @param {Language} language
 * @param {String} description
 * @return {Future}
 * @resolve to true
 * @reject {TypeError|ApiError}
 * @cancel
 */
function setDescription(questionnaire, language, description) {
    if (questionnaire.languageData.currentLanguage.equals(language)) {
        questionnaire.description = description;
    }

    // Error after setting description so that the app can be demonstrated with-
    // out API.
    // TODO: set description via api in given language
    return Future.reject("Please implement this.");
}

/**
 * Set the Questionaire's isPublic property.
 *
 * @param {Questionnaire} questionnaire
 * @param {Boolean} isPublic
 * @return {Future}
 * @resolve to true
 * @reject {TypeError|ApiError}
 * @cancel
 */
function setIsPublic(questionnaire, isPublic) {
    questionnaire.isPublic = isPublic;

    // Error after setting so that the app can be demonstrated without API.
    // TODO: set via API
    return Future.reject("Please implement this.");
}

/**
 * Set the Questionaire's allowEmbedded property.
 *
 * @param {Questionnaire} questionnaire
 * @param {Boolean} allowEmbedded
 * @return {Future}
 * @resolve to true
 * @reject {TypeError|ApiError}
 * @cancel
 */
function setAllowEmbedded(questionnaire, allowEmbedded) {
    questionnaire.allowEmbedded = allowEmbedded;

    // Error after setting so that the app can be demonstrated without API.
    // TODO: set via API
    return Future.reject("Please implement this.");
}

/**
 * Set the Questionaire's xapiTarget property.
 *
 * @param {Questionnaire} questionnaire
 * @param {String} xapiTarget
 * @return {Future}
 * @resolve to true
 * @reject {TypeError|ApiError}
 * @cancel
 */
function setXapiTarget(questionnaire, xapiTarget) {
    questionnaire.xapiTarget = xapiTarget;

    // Error after setting so that the app can be demonstrated without API.
    // TODO: set via API
    return Future.reject("Please implement this.");
}

/**
 * Adds a new ConcreteDimension to a ConcreteQuestionnaire.
 * Uses the Questionnaire's currentLanguage.
 *
 * @param {ConcreteQuestionnaire} questionnaire
 * @param {DataClient} owner
 * @param {String} name
 * @param {Boolean} randomizeQuestions
 * @return {Future}
 * @resolve to true
 * @reject {TypeError|ApiError}
 * @cancel
 */
function addConcreteDimension(questionnaire, owner, name, randomizeQuestions) {
    // TODO: add via API
    // TODO: retrieve correct href
    const href = "";
    // TODO: retrieve correct id
    const id = "";
    const language = questionnaire.languageData.currentLanguage;
    const languageData = new LanguageData(language, language, [language]);

    questionnaire.dimensions.push(new ConcreteDimension(
        href,
        id,
        owner,
        languageData,
        name,
        [],
        randomizeQuestions,
        0,
        []
    ));

    return Future.reject("Please implement this.");
}

/**
 * Adds a new ShadowDimension to a ConcreteQuestionnaire based on a given Con-
 * creteDimension.
 *
 * @param {ConcreteQuestionnaire} questionnaire
 * @param {DataClient} owner
 * @param {ConcreteDimension} dimension
 * @return {Future}
 * @resolve true
 * @reject {TypeError|ApiError}
 * @cancel
 */
function addShadowDimension(questionnaire, owner, dimension) {
    // TODO: add via API
    // TODO: retrieve correct href
    const href = "";
    // TODO: retrieve correct id
    const id = "";
    const languageData = new LanguageData(
        dimension.languageData.currentLanguage,
        dimension.languageData.originalLanguage,
        [...dimension.languageData.availableLanguages]
    );
    // TODO: retrieve ShadowQuestions
    const shadowQuestions = [];

    // Reload so that the new references are respected
    // TODO: build chain around this Future
    reloadDimension(dimension);

    questionnaire.dimensions.push(new ShadowDimension(
        href,
        id,
        owner,
        languageData,
        dimension.name,
        shadowQuestions,
        dimension.randomizeQuestions,
        dimension
    ));

    return Future.reject("Please implement this.");
}

/**
 * Removes a Dimension from a ConcreteQuestionnaire and deletes it.
 *
 * @param {ConcreteQuestionnaire} questionnaire
 * @param {Dimension} dimension
 * @return {Future}
 * @resolve true
 * @reject {TypeError|ApiError}
 * @cancel
 */
function removeDimension(questionnaire, dimension) {
    if (contains(dimension, questionnaire.dimensions)) {
        // TODO: delete via API
        questionnaire.dimensions = without(
            [dimension],
            questionnaire.dimensions
        );
        return Future.of(true);
    } else {
        return Future.reject("Dimension not contained in Questionnaire.");
    }
}

export {
    createConcreteQuestionnaire,
    createShadowQuestionnaire,
    fetchQuestionnaire,
    deleteQuestionnaire,
    fetchTranslation,
    setName,
    setDescription,
    setIsPublic,
    setAllowEmbedded,
    setXapiTarget,
    addConcreteDimension,
    addShadowDimension,
    removeDimension
};
