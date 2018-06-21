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
import {LanguageData} from "../model/Language";

const properties = [
    "name", "description", "isPublic", "allowEmbedded", "xapiTarget"
];

const concreteProperties = [
    "name", "description"
];

/**
 * Create a new ConcreteQuestionnaire.
 *
 * TODO: is owner parameter necessary?
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
 * Since this creates a new reference to the given Questionnaire, it should be
 * updated or reloaded afterwards.
 *
 * TODO: is owner parameter necessary?
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
 * Updates the Questionnaire's fields. If a field is translatable, it is set
 * in the given language.
 *
 * Only allowed parameters are passed.
 * I.e. name and description can only be updated on ConcreteQuestionnaires.
 *
 * @param {Questionnaire} questionnaire
 * @param {Language} language
 * @param {Object} params
 *
 * @return {Future}
 * @resolve {Questionnaire}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function updateQuestionnaire(questionnaire, language, params) {
    const filteredParams = {};
    for (const key in params) {
        // If it is a concrete property, it can only be set on a Concrete-
        // Questionnaire
        if (contains(key, concreteProperties)) {
            if (questionnaire.isConcrete) {
                filteredParams[key] = params[key];
            }
        } else if (contains(key, properties)) {
            filteredParams[key] = params[key];
        }
    }

    // TODO: set props via api and return new Questionnaire

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
 * Adds a new ConcreteDimension to a ConcreteQuestionnaire.
 * Uses the Questionnaire's currentLanguage.
 *
 * The Questionnaire has to be updated or reloaded afterwards, so that the Di-
 * mension appears.
 *
 * @param {ConcreteQuestionnaire} questionnaire
 * TODO: is owner parameter necessary?
 * @param {DataClient} owner
 * @param {String} name
 * @param {Boolean} randomizeQuestions
 *
 * @return {Future}
 * @resolve {ConcreteDimension}
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

    return Future.of(new ConcreteDimension(
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
}

/**
 * Adds a new ShadowDimension to a ConcreteQuestionnaire based on a given Con-
 * creteDimension.
 *
 * The ConcreteQuestionnaire has to be updated or reloaded afterwards, so that
 * the Dimension appears.
 * The ConcreteDimension also has to be uptadet or reloaded, so that its new
 * reference appears.
 *
 * @param {ConcreteQuestionnaire} questionnaire
 * TODO: is owner parameter necessary?
 * @param {DataClient} owner
 * @param {ConcreteDimension} dimension
 *
 * @return {Future}
 * @resolve {ShadowDimension}
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

    return Future.of(new ShadowDimension(
        href,
        id,
        owner,
        languageData,
        dimension.name,
        shadowQuestions,
        dimension.randomizeQuestions,
        dimension
    ));
}

/**
 * Removes a Dimension from a ConcreteQuestionnaire and deletes it.
 *
 * The ConcreteQuestionnaire has to be replaced afterwards to reflect
 * the changes.
 *
 * @param {ConcreteQuestionnaire} questionnaire
 * @param {Dimension} dimension
 *
 * @return {Future}
 * @resolve {Boolean} to true
 * @reject {TypeError|ApiError}
 * @cancel
 *
 * TODO: is the resolve value sensible? Should this maybe resolve with the updated ConcreteQuestionnaire? Define API behavior.
 */
function removeDimension(questionnaire, dimension) {
    if (contains(dimension, questionnaire.dimensions)) {
        // TODO: delete via API
        return Future.of(true);
    } else {
        return Future.reject("Dimension not contained in Questionnaire.");
    }
}

export {
    createConcreteQuestionnaire,
    createShadowQuestionnaire,
    fetchQuestionnaire,
    updateQuestionnaire,
    deleteQuestionnaire,
    addConcreteDimension,
    addShadowDimension,
    removeDimension
};
