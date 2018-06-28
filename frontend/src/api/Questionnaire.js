import Future from "fluture";
import {contains, map, path, pipe, prop, without} from "ramda";

import {extractJson} from "./Util/Response";
import {fetchApi} from "./Util/Request";
import {parseDimension, parseQuestionnaire} from "./Util/Parse";
import {updateDimension} from "./Dimension";

import {
    ConcreteQuestionnaire,
    ShadowQuestionnaire
} from "../model/SurveyBase/Questionnaire";
import {ConcreteDimension} from "../model/SurveyBase/Dimension";

const properties = [
    "name", "description", "isPublic", "allowEmbedded", "xapiTarget"
];

const concreteProperties = [
    "name", "description"
];

/**
 * Create a new ConcreteQuestionnaire.
 *
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
function createConcreteQuestionnaire(language,
                                     name,
                                     description,
                                     isPublic,
                                     allowEmbedded,
                                     xapiTarget = "") {
    const creationData = {
        name,
        description
    };
    const patchData = {
        published: isPublic,
        "allow_embedded": allowEmbedded,
        "xapi_target": xapiTarget
    };
    // First create the ConcreteQuestionnaire with initial data
    return fetchApi(
        "/api/dataclient/concrete_questionnaire",
        {
            method: "POST",
            authenticate: true,
            body: JSON.stringify(creationData),
            language
        }
    )
        .chain(extractJson)
        .map(pipe(prop("questionnaire"), parseQuestionnaire))
        // Then update it with the rest of the data
        .chain(questionnaire => updateQuestionnaire(
            questionnaire, language, patchData
        ));
}

/**
 * Creates a new ShadowQuestionnaire based on the given ConcreteQuestionnaire.
 *
 * Since this creates a new reference to the given Questionnaire, it should be
 * updated or reloaded afterwards.
 *
 * @param {ConcreteQuestionnaire} questionnaire
 * @return {Future}
 * @resolve {ShadowQuestionnaire}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function createShadowQuestionnaire(questionnaire) {
    return fetchApi(
        "/api/dataclient/shadow_questionnaire",
        {
            method: "POST",
            body: JSON.stringify({
                id: questionnaire.id
            }),
            authenticate: true
        }
    )
        .chain(extractJson)
        .map(pipe(prop("questionnaire"), parseQuestionnaire));
}

/**
 * Fetches the Questionnaires belonging to the authorized DataClient in the gi-
 * ven language.
 *
 * @param {Language} language
 * @returns {Future}
 * @resolve {Array<Questionnaire>}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function fetchMyQuestionnaires(language) {
    return fetchApi("/api/dataclient/questionnaire", {authenticate: true})
        .chain(extractJson)
        .map(map(parseQuestionnaire));
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
function fetchQuestionnaire(href, language = null) {
    return fetchApi(
        href,
        {
            language,
            authenticate: true
        })
        .chain(extractJson)
        .map(parseQuestionnaire);
}

/**
 * Fetches a Questionnaire by a given id and build its href.
 *
 * @param {String} id
 * @param {Language} language
 * @returns {Future}
 * @resolve {Questionnaire}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function fetchQuestionnaireById(id, language = null) {
    return fetchQuestionnaire(`/api/questionnaire/${id}`, language);
}

/**
 * Fetches a list of all available template Questionnaires.
 *
 * @param {Language} language on optional language in which the list should be
 *  retrieved
 * @returns {Future}
 * @resolve {Array<ConcreteQuestionnaire>}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function fetchQuestionnaireTemplates(language = null) {
    return fetchApi(
        "/api/questionnaire/template",
        {
            authenticate: true,
            language
        }
    )
        .chain(extractJson)
        .map(map(parseQuestionnaire));
}

/**
 * Updates the Questionnaire's fields. If a field is translatable, it is set
 * in the given language.
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
    return fetchApi(
        questionnaire.href,
        {
            method: "PATCH",
            authenticate: true,
            body: JSON.stringify(params),
            language
        }
    )
        .chain(extractJson)
        .map(pipe(prop("questionnaire"), parseQuestionnaire));
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
    return fetchApi(
        questionnaire.href,
        {
            method: "DELETE",
            authenticate: true
        }
    )
        .map(() => true);
}

/**
 * Adds a new ConcreteDimension to a ConcreteQuestionnaire.
 * Uses the Questionnaire's currentLanguage.
 *
 * The Questionnaire has to be updated or reloaded afterwards, so that the Di-
 * mension appears.
 *
 * @param {ConcreteQuestionnaire} questionnaire
 * @param {String} name
 * @param {Boolean} randomizeQuestions
 *
 * @return {Future}
 * @resolve {ConcreteDimension}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function addConcreteDimension(questionnaire, name, randomizeQuestions) {
    return fetchApi(
        questionnaire.href + "/concrete_dimension",
        {
            method: "POST",
            authenticate: true,
            body: JSON.stringify({name}),
            language: questionnaire.languageData.currentLanguage
        }
    )
        .chain(extractJson)
        .map(pipe(prop("dimension"), parseDimension))
        // Update dimension with non-initial parameters after creation
        .chain(dimension => updateDimension(
            dimension,
            questionnaire.languageData.currentLanguage,
            {randomizeQuestions}
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
 * @param {ConcreteDimension} dimension
 *
 * @return {Future}
 * @resolve {ShadowDimension}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function addShadowDimension(questionnaire, dimension) {
    return fetchApi(
        questionnaire.href + "/shadow_dimension",
        {
            method: "POST",
            authenticate: true,
            body: {id: questionnaire.id}
        }
    )
        .chain(extractJson)
        .map(pipe(prop("dimension"), parseDimension));
}

/**
 * Removes a Dimension from a ConcreteQuestionnaire and deletes it.
 *
 * The ConcreteQuestionnaire has to be updated or reloaded afterwards to reflect
 * the changes.
 *
 * @param {ConcreteQuestionnaire} questionnaire
 * @param {Dimension} dimension
 *
 * @return {Future}
 * @resolve {Boolean} to true
 * @reject {TypeError|ApiError}
 * @cancel
 */
function removeDimension(questionnaire, dimension) {
    if (contains(dimension, questionnaire.dimensions)) {
        return fetchApi(
            dimension.href,
            {
                method: "DELETE",
                authenticate: true
            }
        )
            .map(() => true);
    } else {
        return Future.reject("Dimension not contained in Questionnaire.");
    }
}

/**
 * Takes in a Questionnaire and populates its incoming references field by re-
 * placing all resolvable References with their corresponding ShadowQuestion-
 * naire instances.
 *
 * Accesses the API to load the Questionnaires.
 *
 * If this rejects, then some questionnaires might be populated and some might
 * still be Resources. The exact state will have to be tested.
 *
 * @param {ConcreteQuestionnaire} concreteQuestionnaire
 * @return {Future}
 * @resolve {Array<ShadowQuestionnaire>}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function populateOwnedIncomingReferences(concreteQuestionnaire) {
    const resolvedShadowQuestionnaireFutures = [];

    // Use basic for loop to easily replace values.
    for (let i = 0;
         i < concreteQuestionnaire.ownedIncomingReferences.length;
         i++) {
        let reference = concreteQuestionnaire.ownedIncomingReferences[i];

        if (instanceOf(reference, Resource)) {
            const shadowQuestionnaireFuture = fetchQuestionnaire(
                reference.href,
                concreteQuestionnaire.languageData.currentLanguage
            )
                .chain(shadowQuestionnaire => {
                    concreteQuestionnaire.ownedIncomingReferences[i] =
                        shadowQuestionnaire;
                    return Future.of(shadowQuestionnaire);
                });

            resolvedShadowQuestionnaireFutures.push(shadowQuestionnaireFuture);
        }
    }
    // MAYBE: is Infinity appropriate?
    return Future.parallel(Infinity, resolvedShadowQuestionnaireFutures);
}

/**
 * If the referenceTo field contains a Resource, it is resolved to a
 * ConcreteQuestionnaire instance. Otherwise it is left as is.
 *
 * Accesses the API to load the Questionnaire.
 *
 * @param {ShadowQuestionnaire} shadowQuestionnaire
 * @return {Future}
 * @resolve {ConcreteQuestionnaire}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function populateReferenceTo(shadowQuestionnaire) {
    if (instanceOf(shadowQuestionnaire.referenceTo, Resource)) {
        return fetchQuestionnaire(
            shadowQuestionnaire.referenceTo.href,
            shadowQuestionnaire.languageData.currentLanguage
        )
            .chain(concreteQuestionnaire => {
                shadowQuestionnaire.referenceTo = concreteQuestionnaire;
                return Future.of(concreteQuestionnaire);
            });
    }
    return Future.of(shadowQuestionnaire.referenceTo);
}

/**
 * Based on the type of the given Questionnaire this either populates its inco-
 * ming references or its referenceTo field.
 *
 * @param {Questionnaire} questionnaire
 * @return {Future}
 * @resolve {Array<ShadowQuestionnaire>|ConcreteQuestionnaire}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function populateQuestionnaire(questionnaire) {
    if (instanceOf(questionnaire, ShadowQuestionnaire)) {
        return populateReferenceTo(questionnaire);
    }
    if (instanceOf(questionnaire, ConcreteQuestionnaire)) {
        return populateOwnedIncomingReferences(questionnaire);
    }
}

export {
    createConcreteQuestionnaire,
    createShadowQuestionnaire,
    fetchMyQuestionnaires,
    fetchQuestionnaire,
    fetchQuestionnaireById,
    fetchQuestionnaireTemplates,
    updateQuestionnaire,
    deleteQuestionnaire,
    addConcreteDimension,
    addShadowDimension,
    removeDimension,
    populateOwnedIncomingReferences,
    populateReferenceTo,
    populateQuestionnaire
};
