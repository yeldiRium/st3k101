import Future from "fluture";
import {contains, without} from "ramda";

import {
    ConcreteDimension,
    ShadowDimension
} from "../model/SurveyBase/Dimension";
import {ConcreteQuestion, ShadowQuestion} from "../model/SurveyBase/Question";
import {LanguageData} from "../model/Language";

const properties = ["name", "randomizeQuestions"];

const concreteProperties = ["name"];

/**
 * Fetches a Dimension by a given href in the given language.
 *
 * @param {String} href
 * @param {Language} language
 *
 * @return {Future}
 * @resolve {Dimension}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function fetchDimension(href, language) {
    // TODO: fetch Dimension from API
    return Future.reject("Please implement this.");
}

/**
 * Updates the Dimension's fields. If a field is translatable, it is set
 * in the given language.
 *
 * Only allowed parameters are passed.
 * I.e. name and description can only be updated on ConcreteDimensions.
 *
 * @param {Dimension} dimension
 * @param {Language} language
 * @param {Object} params
 *
 * @return {Future}
 * @resolve {Dimension}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function updateDimension(dimension, language, params) {
    const filteredParams = {};
    for (const key in params) {
        // If it is a concrete property, it can only be set on a Concrete-
        // Dimension
        if (contains(key, concreteProperties)) {
            if (dimension.isConcrete) {
                filteredParams[key] = params[key];
            }
        } else if (contains(key, properties)) {
            filteredParams[key] = params[key];
        }
    }

    // TODO: set props via api and return new Dimension

    return Future.reject("Please implement this.");
}

/**
 * Add a new ConcreteQuestion to the Dimension.
 * Uses the Dimension's currentLanguage.
 *
 * The Dimension has to be updated or reloaded afterwards, so that the
 * new Question appears.
 *
 * @param {ConcreteDimension} dimension
 * TODO: is owner parameter necessary?
 * @param {DataClient} owner
 * @param {String} text
 * @param {Range} range
 * @return Future
 * @resolve {ShadowQuestionnaire}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function addConcreteQuestion(dimension, owner, text, range) {
    // TODO: create via API
    // TODO: retrieve correct href
    const href = (Math.random() + 1).toString(36);
    // TODO: retrieve correct id
    const id = href;
    const language = dimension.languageData.currentLanguage;
    const languageData = new LanguageData(language, language, [language]);

    return Future.of(new ConcreteQuestion(
        href,
        id,
        [owner],
        languageData,
        text,
        range,
        0,
        []
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
 * @param {ConcreteDimension} dimension
 * TODO: is owner parameter necessary?
 * @param {DataClient} owner
 * @param {ConcreteQuestion} question
 * @return Future
 * @resolve {ShadowQuestionnaire}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function addShadowQuestion(dimension, owner, question) {
    // TODO: create via API
    // TODO: retrieve correct href
    const href = (Math.random() + 1).toString(36);
    // TODO: retrieve correct id
    const id = href;
    const languageData = new LanguageData(
        question.languageData.currentLanguage,
        question.languageData.originalLanguage,
        [...question.languageData.availableLanguages]
    );

    return Future.of(new ShadowQuestion(
        href,
        id,
        [owner],
        languageData,
        question.text,
        question.range.clone(),
        question
    ));
}

/**
 * Removes the question from the dimension by deleting the question.
 *
 * The ConcreteDimension has to be updated or reloaded afterwards to reflect
 * the changes.
 *
 * @param {ConcreteDimension} dimension
 * @param {Question} question
 * @return {Future}
 * @resolve to true
 * @reject {TypeError|ApiError}
 * @cancel
 *
 * TODO: is the resolve value sensible? Should this maybe resolve with the updated ConcreteDimension? Define API behavior.
 */
function removeQuestion(dimension, question) {
    if (contains(question, dimension.questions)) {
        // TODO: delete via API
        return Future.of(true);
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
 * @param {ConcreteDimension} concreteDimension
 * @return {Future}
 * @resolve {Array<ShadowDimension>}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function populateOwnedIncomingReferences(concreteDimension) {
    const resolvedShadowDimensionFutures = [];

    // Use basic for loop to easily replace values.
    for (let i = 0; i < concreteDimension.ownedIncomingReferences.length; i++) {
        let reference = concreteDimension.ownedIncomingReferences[i];

        if (instanceOf(reference, Resource)) {
            const shadowDimensionFuture = fetchDimension(
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
 * @param {ShadowDimension} shadowDimension
 * @return {Future}
 * @resolve {ConcreteDimension}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function populateReferenceTo(shadowDimension) {
    if (instanceOf(shadowDimension.referenceTo, Resource)) {
        return fetchDimension(
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
 * @param {Dimension} dimension
 * @return {Future}
 * @resolve {Array<ShadowDimension>|ConcreteDimension}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function populateDimension(dimension) {
    if (instanceOf(dimension, ShadowDimension)) {
        return populateReferenceTo(dimension);
    }
    if (instanceOf(dimension, ConcreteDimension)) {
        return populateOwnedIncomingReferences(dimension);
    }
}

export {
    fetchDimension,
    updateDimension,
    addConcreteQuestion,
    addShadowQuestion,
    removeQuestion,
    populateOwnedIncomingReferences,
    populateReferenceTo,
    populateDimension
};
