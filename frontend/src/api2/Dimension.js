import Future from "fluture";
import {contains, without} from "ramda";

import {ConcreteDimension} from "../model/SurveyBase/Dimension";
import {ConcreteQuestion, ShadowQuestion} from "../model/SurveyBase/Question";
import {reloadQuestion} from "./Question";
import {LanguageData} from "../model/Language";

/**
 * Reload the Dimension's data in its current language.
 *
 * @param {Dimension} dimension
 * @return {Future}
 * @resolve to true
 * @reject with an API error message
 * @cancel TODO: is this cancellable?
 */
function reloadDimension(dimension) {
    // TODO: reload via API
    return Future.reject("Please implement this.");
}

/**
 * Fetches the Dimension from the API in the requested language.
 * Updates all translatable information in place and updates the
 * `languageData` object.
 *
 * Should also check, if the list of availableLanguages has changed and
 * overwrite the old one.
 *
 * @param {Dimension} dimension
 * @param {Language} language
 * @return Future
 * @resolve to true
 * @reject with an API error message, if something went wrong
 * @cancel TODO: is this cancellable?
 */
function fetchTranslation(dimension, language) {
    // TODO: fetch translation from api
    // TODO: set languageData in dimension
    // TODO: set translated fields in dimension
    return Future.reject("Please implement this.");
}

/**
 * Sets the Dimension's name in the given language. Adds a new available langu-
 * age to the Dimension, if it doesn't exist yet.
 *
 * If it is the currentLanguage, the Dimension is updated with the new text.
 *
 * @param {ConcreteDimension} dimension
 * @param {Language} language
 * @param {String} name
 * @return {Future}
 * @resolve to true
 * @reject with an API error message
 * @cancel TODO: is this cancellable?
 */
function setName(dimension, language, name) {
    // Overwrite current name, if the language is the currently selected one
    if (dimension.languageData.currentLanguage.equals(language)) {
        dimension.name = name;
    }

    // Error after setting name so that the app can be demonstrated without API.
    // TODO: set name via api in given language
    return Future.reject("Please implement this.");
}

/**
 * Sets the "randomizeQuestions" property.
 *
 * @param {Dimension} dimension
 * @param {Boolean} randomizeQuestions
 * @return {Future}
 * @resolve to true
 * @reject with API error message
 * @cancel TODO: is this cancellable?
 */
function setRandomizeQuestions(dimension, randomizeQuestions) {
    // Set before throwing error so that the app can be used for demos.
    dimension.randomizeQuestions = randomizeQuestions;

    // TODO: set prop via API
    return Future.reject("Please implement this.");
}

/**
 * Add a new ConcreteQuestion to the Dimension.
 * Uses the Dimension's currentLanguage.
 *
 * @param {ConcreteDimension} dimension
 * @param {DataClient} owner
 * @param {String} text
 * @param {Range} range
 * @return Future
 * @resolve {ShadowQuestionnaire}
 * @reject with an API error message, if something went wrong
 * @cancel TODO: is this cancellable?
 */
function addConcreteQuestion(dimension, owner, text, range) {
    // TODO: create via API
    // TODO: retrieve correct href
    const href = "";
    const language = dimension.languageData.currentLanguage;
    const languageData = new LanguageData(
        language,
        language,
        [language]
    );

    dimension.questions.push(new ConcreteQuestion(
        href,
        owner,
        languageData,
        text,
        range,
        0,
        []
    ));

    return Future.reject("Please implement this.");
}

/**
 * Add a new ShadowQuestion based on the given ConcreteQuestion to the Dimen-
 * sion.
 *
 * @param {ConcreteDimension} dimension
 * @param {DataClient} owner
 * @param {ConcreteQuestion} question
 * @return Future
 * @resolve {ShadowQuestionnaire}
 * @reject with an API error message, if something went wrong
 * @cancel TODO: is this cancellable?
 */
function addShadowQuestion(dimension, owner, question) {
    // TODO: create via API
    // TODO: retrieve correct href
    const href = "";
    const languageData = new LanguageData(
        question.languageData.currentLanguage,
        question.languageData.originalLanguage,
        [...question.languageData.availableLanguages]
    );

    // Reload so that the references are respected.
    // TODO: build chain around this Future
    reloadQuestion(question);

    dimension.questions.push(new ShadowQuestion(
        href,
        owner,
        languageData,
        question.text,
        question.range.clone(),
        question
    ));

    return Future.reject("Please implement this.");
}

/**
 * Removes the question from the dimension by deleting the question.
 *
 * @param {ConcreteDimension} dimension
 * @param {Question} question
 * @return {Future}
 * @resolve to true
 * @reject with API error message
 * @cancel TODO: is this cancellable?
 */
function removeQuestion(dimension, question) {
    if (contains(question, dimension.questions)) {
        // TODO: delete via API
        dimension.questions = without([question], dimension.questions);
    } else {
        return Future.reject("Question not contained in Dimension.");
    }
}

export {
    reloadDimension,
    fetchTranslation,
    setName,
    setRandomizeQuestions,
    addConcreteQuestion,
    addShadowQuestion,
    removeQuestion
};