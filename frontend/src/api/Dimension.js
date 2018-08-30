import Future from "fluture";
import {
    assoc,
    clone,
    contains,
    dissoc,
    has,
    map,
    pipe,
    prop,
    without
} from "ramda";

import {fetchApi} from "./Util/Request";
import {extractJson} from "./Util/Response";
import {updateQuestion} from "./Question";
import {parseDimension, parseQuestion} from "./Util/Parse";

import {
    ConcreteDimension,
    ShadowDimension
} from "../model/SurveyBase/Dimension";
import {ConcreteQuestion} from "../model/SurveyBase/Question";
import renameProp from "./Util/renameProp";

const properties = ["name", "randomizeQuestions"];

const concreteProperties = ["name"];

/**
 * Fetches a Dimension by a given href in the given language.
 *
 * @param {String} authenticationToken
 * @param {String} href
 * @param {Language} language
 *
 * @return {Future}
 * @resolve {Dimension}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function fetchDimension(authenticationToken, href, language = null) {
    return fetchApi(
        href,
        {
            authenticationToken,
            language
        }
    )
        .chain(extractJson)
        .map(parseDimension);
}

/**
 * Fetches a Dimension by building its href from its id in the given language.
 *
 * @param {String} authenticationToken
 * @param {String} id
 * @param {Language} language
 *
 * @return {Future}
 * @resolve {Dimension}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function fetchDimensionById(authenticationToken, id, language = null) {
    return fetchDimension(authenticationToken, `/api/dimension/${id}`, language);
}

/**
 * Fetches a list of all available template Dimensions.
 *
 * @param {String} authenticationToken
 * @param {Language} language on optional language in which the list should be
 *  retrieved
 * @returns {Future}
 * @resolve {Array<ConcreteDimension>}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function fetchDimensionTemplates(authenticationToken, language = null) {
    return fetchApi(
        "/api/dimension/template",
        {
            authenticationToken,
            language
        }
    )
        .chain(extractJson)
        .map(map(parseDimension));
}

/**
 * Updates the Dimension's fields. If a field is translatable, it is set
 * in the given language.
 *
 * @param {String} authenticationToken
 * @param {Dimension} dimension
 * @param {Language} language
 * @param {Object} params
 *
 * @return {Future}
 * @resolve {Dimension}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function updateDimension(authenticationToken, dimension, language, params) {
    let parsedParams = pipe(
        renameProp("randomizeQuestions", "randomize_question_order"),
        renameProp("referenceId", "reference_id")
    )(params);

    return fetchApi(
        dimension.href,
        {
            method: "PATCH",
            authenticationToken,
            body: JSON.stringify(parsedParams),
            language
        }
    )
        .chain(extractJson)
        .map(pipe(prop("dimension"), parseDimension));
}

/**
 * Add a new ConcreteQuestion to the Dimension.
 * Uses the Dimension's currentLanguage.
 *
 * The Dimension has to be updated or reloaded afterwards, so that the
 * new Question appears.
 *
 * @param {String} authenticationToken
 * @param {ConcreteDimension} dimension
 * @param {String} text
 * @param {Range} range
 * @return Future
 * @resolve {ShadowQuestionnaire}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function addConcreteQuestion(authenticationToken, dimension, text, range) {
    return fetchApi(
        dimension.href + "/concrete_question",
        {
            method: "POST",
            authenticationToken,
            body: JSON.stringify({text}),
            language: dimension.languageData.currentLanguage
        }
    )
        .chain(extractJson)
        .map(pipe(prop("question"), parseQuestion))
        .chain(question => updateQuestion(
            question,
            dimension.languageData.currentLanguage,
            {range}
        ));
}

/**
 * Add a new ShadowQuestion based on the given ConcreteQuestion to the Dimen-
 * sion.
 *
 *
 * The ConcreteDimension has to be updated or reloaded afterwards, so that
 * the Question appears.
 * The ConcreteQuestion must be updated or reloaded afterwards to reflect the
 * increase in references
 *
 * @param {String} authenticationToken
 * @param {ConcreteDimension} dimension
 * @param {ConcreteQuestion} question
 * @return {Future}
 * @resolve {ShadowQuestionnaire}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function addShadowQuestion(authenticationToken, dimension, question) {
    return fetchApi(
        dimension.href + "/shadow_question",
        {
            method: "POST",
            authenticationToken,
            body: JSON.stringify({id: question.id})
        }
    )
        .chain(extractJson)
        .map(pipe(prop("question"), parseQuestion));
}

/**
 * Removes the question from the dimension by deleting the question.
 *
 * The ConcreteDimension has to be updated or reloaded afterwards to reflect
 * the changes.
 *
 * @param {String} authenticationToken
 * @param {ConcreteDimension} dimension
 * @param {Question} question
 * @return {Future}
 * @resolve {Boolean} to true
 * @reject {TypeError|ApiError}
 * @cancel
 */
function removeQuestion(authenticationToken, dimension, question) {
    if (contains(question, dimension.questions)) {
        return fetchApi(
            question.href,
            {
                method: "DELETE",
                authenticationToken
            }
        )
            .map(() => true);
    } else {
        return Future.reject("Question not contained in Dimension.");
    }
}

/**
 * Takes in a Dimension and populates its incoming references field by replacing
 * all resolvable References with their corresponding ShadowDimension instances.
 *
 * Accesses the API to load the Dimensions.
 *
 * If this rejects, then some dimensions might be populated and some might still
 * be Resources. The exact state will have to be tested.
 *
 * @param {String} authenticationToken
 * @param {ConcreteDimension} concreteDimension
 * @return {Future}
 * @resolve {Array<ShadowDimension>}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function populateOwnedIncomingReferences(authenticationToken, concreteDimension) {
    const resolvedShadowDimensionFutures = [];

    // Use basic for loop to easily replace values.
    for (let i = 0; i < concreteDimension.ownedIncomingReferences.length; i++) {
        let reference = concreteDimension.ownedIncomingReferences[i];

        if (instanceOf(reference, Resource)) {
            const shadowDimensionFuture = fetchDimension(
                authenticationToken,
                reference.href,
                concreteDimension.languageData.currentLanguage
            )
                .chain(shadowDimension => {
                    concreteDimension.ownedIncomingReferences[i] =
                        shadowDimension;
                    return Future.of(shadowDimension);
                });

            resolvedShadowDimensionFutures.push(shadowDimensionFuture);
        }
    }
    // MAYBE: is Infinity appropriate?
    return Future.parallel(Infinity, resolvedShadowDimensionFutures);
}

/**
 * If the referenceTo field contains a Resource, it is resolved to a
 * ConcreteDimension instance. Otherwise it is left as is.
 *
 * Accesses the API to load the Dimension.
 *
 * @param {String} authenticationToken
 * @param {ShadowDimension} shadowDimension
 * @return {Future}
 * @resolve {ConcreteDimension}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function populateReferenceTo(authenticationToken, shadowDimension) {
    if (instanceOf(shadowDimension.referenceTo, Resource)) {
        return fetchDimension(
            authenticationToken,
            shadowDimension.referenceTo.href,
            shadowDimension.languageData.currentLanguage
        )
            .chain(concreteDimension => {
                shadowDimension.referenceTo = concreteDimension;
                return Future.of(concreteDimension);
            });
    }
    return Future.of(shadowDimension.referenceTo);
}

/**
 * Based on the type of the given Dimension this either populates its incoming
 * references or its referenceTo field.
 *
 * @param {String} authenticationToken
 * @param {Dimension} dimension
 * @return {Future}
 * @resolve {Array<ShadowDimension>|ConcreteDimension}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function populateDimension(authenticationToken, dimension) {
    if (instanceOf(dimension, ShadowDimension)) {
        return populateReferenceTo(authenticationToken, dimension);
    }
    if (instanceOf(dimension, ConcreteDimension)) {
        return populateOwnedIncomingReferences(authenticationToken, dimension);
    }
}

export {
    fetchDimension,
    fetchDimensionById,
    fetchDimensionTemplates,
    updateDimension,
    addConcreteQuestion,
    addShadowQuestion,
    removeQuestion
};
