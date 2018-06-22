import Future from "fluture";
import {contains} from "ramda";

import Question, {
    ConcreteQuestion,
    ShadowQuestion
} from "../model/SurveyBase/Question";

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

/**
 * Takes in a Question and populates its incoming references field by replacing
 * all resolvable References with their corresponding ShadowQuestion instances.
 *
 * Accesses the API to load the Questions.
 *
 * If this rejects, then some questions might be populated and some might still
 * be Resources. The exact state will have to be tested.
 *
 * @param {ConcreteQuestion} concreteQuestion
 * @return {Future}
 * @resolve {Array<ShadowQuestion>}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function populateOwnedIncomingReferences(concreteQuestion) {
    const resolvedShadowQuestionFutures = [];

    // Use basic for loop to easily replace values.
    for (let i = 0; i < concreteQuestion.ownedIncomingReferences.length; i++) {
        /** @type {Resource|ShadowQuestion} */
        let reference = concreteQuestion.ownedIncomingReferences[i];

        if (instanceOf(reference, Resource)) {
            const shadowQuestionFuture = fetchQuestion(
                reference.href,
                concreteQuestion.languageData.currentLanguage
            )
                .chain(shadowQuestion => {
                    concreteQuestion.ownedIncomingReferences[i] =
                        shadowQuestion;
                    return Future.of(shadowQuestion);
                });

            resolvedShadowQuestionFutures.push(shadowQuestionFuture);
        }
    }
    // MAYBE: is Infinity appropriate?
    return Future.parallel(Infinity, resolvedShadowQuestionFutures);
}

/**
 * If the referenceTo field contains a Resource, it is resolved to a
 * ConcreteQuestion instance. Otherwise it is left as is.
 *
 * Accesses the API to load the Question.
 *
 * If this rejects, the referenceTo property was not replaced. It might still be
 * a Resource.
 *
 * @param {ShadowQuestion} shadowQuestion
 * @return {Future}
 * @resolve {ConcreteQuestion}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function populateReferenceTo(shadowQuestion) {
    if (instanceOf(shadowQuestion.referenceTo, Resource)) {
        const shadowQuestionFuture = fetchQuestion(
            shadowQuestion.referenceTo.href,
            shadowQuestion.languageData.currentLanguage
        )
            .chain(concreteQuestion => {
                shadowQuestion.referenceTo = concreteQuestion;
                return Future.of(concreteQuestion);
            });
    }
    return Future.of(shadowQuestion.referenceTo);
}

/**
 * Based on the type of the given Question this either populates its incoming
 * references or its referenceTo field.
 *
 * @param {Question} question
 * @return {Future}
 * @resolve {Array<ShadowQuestion>|ConcreteQuestion}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function populateQuestion(question) {
    // Type warnings can be ignored, since they are tested.
    if (instanceOf(question, ShadowQuestion)) {
        return populateReferenceTo(question);
    }
    if (instanceOf(question, ConcreteQuestion)) {
        return populateOwnedIncomingReferences(question);
    }
}

export {
    fetchQuestion,
    updateQuestion,
    populateOwnedIncomingReferences,
    populateReferenceTo,
    populateQuestion
};
