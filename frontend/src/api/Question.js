import Future from "fluture";
import {contains, pipe, prop} from "ramda";

import {extractJson} from "./Util/Response";
import {parseQuestion} from "./Util/Parse";

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
function fetchQuestion(href, language = null) {
    return fetchApi(
        href,
        {
            authenticate: true,
            language
        }
    )
        .chain(extractJson)
        .map(parseQuestion);
}

/**
 * Fetches a Question by building its href from its id in the given language.
 *
 * @param {String} id
 * @param {Language} language
 *
 * @return {Future}
 * @resolve {Question}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function fetchQuestionById(id, language = null) {
    return fetchQuestion(`/api/question/${id}`, language);
}

/**
 * Updates the Question's fields. If a field is translatable, it is set
 * in the given language.
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
    return fetchApi(
        question.href,
        {
            method: "PATCH",
            authenticate: true,
            body: JSON.stringify(params),
            language
        }
    )
        .chain(extractJson)
        .map(pipe(prop("question"), parseQuestion));
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
    fetchQuestionById,
    updateQuestion,
    populateOwnedIncomingReferences,
    populateReferenceTo,
    populateQuestion
};
