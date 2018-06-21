import Future from "fluture";

import Question from "../model/SurveyBase/Question";

/**
 * Retrieves a Question based on href or id.
 *
 * @param href
 * @param id
 * @return {Future}
 * @resolve {Question}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function getQuestion({href, id}) {
    // TODO: fetch Question from API
    console.log("getQuestion");
    // TODO: return test data
    return Future.reject(false);
}

/**
 * Reloads the Question's data in its current language.
 * @param {Question} question
 * @return {Future}
 * @resolve {Boolean} to true
 * @reject {TypeError|ApiError}
 * @cancel
 */
function reloadQuestion(question) {
    // TODO: fetch data from API and rewrite question content
    return Future.reject("Please implement this.");
}

/**
 * Fetches the Question from the API in the requested language.
 * Updates all translatable information in place and updates the
 * `languageData` object.
 *
 * Should also check, if the list of availableLanguages has changed and
 * overwrite the old one.
 *
 * @param {Question} question
 * @param {Language} language
 * @return {Future}
 * @resolve {Boolean} to true
 * @reject {TypeError|ApiError}
 * @cancel
 */
function fetchTranslation(question, language) {
    // TODO: fetch translation from api
    // TODO: set languageData in question
    // TODO: set translated fields in question
    return Future.reject("Please implement this.");
}

/**
 * Sets the Question's text in the given language. Creates a new available
 * language on the Question, if it doesn't exist already.
 *
 * If it is the currentLanguage, the Question is updated with the new text.
 *
 * @param {ConcreteQuestion} question
 * @param {Language} language
 * @param {String} text
 * @return {Future}
 * @resolve {Boolean} to true
 * @reject {TypeError|ApiError}
 * @cancel
 */
function setText(question, language, text) {
    // Overwrite current text, if the language is the currently selected one
    if (question.languageData.currentLanguage.equals(language)) {
        question.text = text;
    }

    // Error after setting text so that the app can be demonstrated without API.
    // TODO: set text via api in given language
    return Future.reject("Please implement this.");
}

/**
 * Sets the Range on the given question.
 *
 * @param {ConcreteQuestion} question
 * @param {Range} range
 * @return {Future}
 * @resolve {Boolean} to true
 * @reject {TypeError|ApiError}
 * @cancel
 */
function setRange(question, range) {
    question.range = range;

    // Error after setting range so that the app can be demonstrated without API.
    // TODO: set range via api
    return Future.reject("Please implement this.");
}

export {
    getQuestion,
    reloadQuestion,
    fetchTranslation,
    setText,
    setRange
};
