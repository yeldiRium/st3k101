import Future from "fluture";
import {contains} from "ramda";

import Question from "../model/SurveyBase/Question";

const properties = ["text", "range"];

const concreteProperties = ["text"];

/**
 * Fetches a Question by a given href in the given language.
 *
 * @param {String} href
 * @param {Language} language
 *
 * @return {Future}
 * @resolve {Question}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function fetchQuestion(href, language) {
    // TODO: fetch Question from API
    return Future.reject("Please implement this.");
}

/**
 * Updates the Question's fields. If a field is translatable, it is set
 * in the given language.
 *
 * Only allowed parameters are passed.
 * I.e. text can only be updated on ConcreteQuestions.
 *
 * @param {Question} question
 * @param {Language} language
 * @param {Object} params
 *
 * @return {Future}
 * @resolve {Question}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function updateQuestion(question, language, params) {
    const filteredParams = {};
    for (const key in params) {
        // If it is a concrete property, it can only be set on a Concrete-
        // Question
        if (contains(key, concreteProperties)) {
            if (question.isConcrete) {
                filteredParams[key] = params[key];
            }
        } else if (contains(key, properties)) {
            filteredParams[key] = params[key];
        }
    }

    // TODO: set props via api and return new Question

    return Future.reject("Please implement this.");
}

export {
    fetchQuestion,
    updateQuestion
};
