import * as Future from "fluture/index.js";
import { contains, map, pipe, prop } from "ramda";

import { extractJson } from "./Util/Response";
import { fetchApi } from "./Util/Request";
import {
  parseDimension,
  parseQuestionnaire,
  parseSubmissionQuestionnaire
} from "./Util/Parse";
import { updateDimension } from "./Dimension";

import {
  ConcreteQuestionnaire,
  ShadowQuestionnaire
} from "../model/SurveyBase/Questionnaire";
import renameProp from "./Util/renameProp";

/**
 * Create a new ConcreteQuestionnaire.
 *
 * @param authenticationToken
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
function createConcreteQuestionnaire(
  authenticationToken,
  language,
  name,
  description,
  isPublic,
  allowEmbedded,
  xapiTarget = null
) {
  const creationData = {
    name,
    description
  };
  let patchData = {
    published: isPublic,
    allow_embedded: allowEmbedded
  };
  if (xapiTarget !== null) {
    patchData["xapi_target"] = xapiTarget;
  }

  // First create the ConcreteQuestionnaire with initial data
  return (
    fetchApi("/api/dataclient/concrete_questionnaire", {
      method: "POST",
      authenticationToken,
      body: JSON.stringify(creationData),
      language
    })
      .chain(extractJson)
      .map(
        pipe(
          prop("questionnaire"),
          parseQuestionnaire
        )
      )
      // Then update it with the rest of the data
      .chain(questionnaire =>
        updateQuestionnaire(
          authenticationToken,
          questionnaire,
          language,
          patchData
        )
      )
  );
}

/**
 * Creates a new ShadowQuestionnaire based on the given ConcreteQuestionnaire.
 *
 * Since this creates a new reference to the given Questionnaire, it should be
 * updated or reloaded afterwards.
 *
 * @param authenticationToken
 * @param {ConcreteQuestionnaire} questionnaire
 * @return {Future}
 * @resolve {ShadowQuestionnaire}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function createShadowQuestionnaire(authenticationToken, questionnaire) {
  return fetchApi("/api/dataclient/shadow_questionnaire", {
    method: "POST",
    authenticationToken,
    body: JSON.stringify({
      id: questionnaire.id
    })
  })
    .chain(extractJson)
    .map(
      pipe(
        prop("questionnaire"),
        parseQuestionnaire
      )
    );
}

/**
 * Fetches the Questionnaires belonging to the authorized DataClient in the gi-
 * ven language.
 *
 * @param authenticationToken
 * @param {Language} language
 * @returns {Future}
 * @resolve {Array<Questionnaire>}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function fetchMyQuestionnaires(authenticationToken, language) {
  return fetchApi("/api/dataclient/questionnaire", {
    authenticationToken,
    language
  })
    .chain(extractJson)
    .map(map(parseQuestionnaire));
}

/**
 * Fetches a Questionnaire by a given href in the given language.
 *
 * @param authenticationToken
 * @param {String} href
 * @param {Language} language
 *
 * @return {Future}
 * @resolve {Questionnaire}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function fetchQuestionnaire(authenticationToken, href, language = null) {
  return fetchApi(href, {
    language,
    authenticationToken
  })
    .chain(extractJson)
    .map(parseQuestionnaire);
}

/**
 * Fetches a Questionnaire by a given id and build its href.
 *
 * @param authenticationToken
 * @param {String} id
 * @param {Language} language
 * @returns {Future}
 * @resolve {Questionnaire}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function fetchQuestionnaireById(authenticationToken, id, language = null) {
  return fetchQuestionnaire(
    authenticationToken,
    `/api/questionnaire/${id}`,
    language
  );
}

/**
 * @param id
 * @param language
 * @returns {Future}
 */
function fetchQuestionnaireForSubmissionById(id, language = null) {
  return fetchApi(`/api/questionnaire/${id}`, {
    language
  })
    .chain(extractJson)
    .map(parseSubmissionQuestionnaire);
}

/**
 * Fetches a list of all available template Questionnaires.
 *
 * @param authenticationToken
 * @param {Language} language on optional language in which the list should be
 *  retrieved
 * @returns {Future}
 * @resolve {Array<ConcreteQuestionnaire>}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function fetchQuestionnaireTemplates(authenticationToken, language = null) {
  return fetchApi("/api/questionnaire/template", {
    authenticationToken,
    language
  })
    .chain(extractJson)
    .map(map(parseQuestionnaire));
}

/**
 * Updates the Questionnaire's fields. If a field is translatable, it is set
 * in the given language.
 *
 * @param authenticationToken
 * @param {Questionnaire} questionnaire
 * @param {Language} language
 * @param {Object} params
 *
 * @return {Future}
 * @resolve {Questionnaire}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function updateQuestionnaire(
  authenticationToken,
  questionnaire,
  language,
  params
) {
  let parsedParams = pipe(
    renameProp("isPublic", "published"),
    renameProp("referenceId", "reference_id"),
    renameProp("xapiTarget", "xapi_target"),
    renameProp("allowEmbedded", "allow_embedded"),
    renameProp("acceptsSubmissions", "accepts_submissions")
  )(params);

  return fetchApi(questionnaire.href, {
    method: "PATCH",
    authenticationToken,
    body: JSON.stringify(parsedParams),
    language
  })
    .chain(extractJson)
    .map(
      pipe(
        prop("questionnaire"),
        parseQuestionnaire
      )
    );
}

/**
 * Delete the Questionnaire and all appended Dimensions.
 *
 * @param authenticationToken
 * @param {Questionnaire} questionnaire
 * @return {Future}
 * @resolve {Boolean} with true
 * @reject {TypeError|ApiError}
 * @cancel
 */
function deleteQuestionnaire(authenticationToken, questionnaire) {
  return fetchApi(questionnaire.href, {
    method: "DELETE",
    authenticationToken
  }).map(() => true);
}

/**
 * Adds a new ConcreteDimension to a ConcreteQuestionnaire.
 * Uses the Questionnaire's currentLanguage.
 *
 * The Questionnaire has to be updated or reloaded afterwards, so that the Di-
 * mension appears.
 *
 * @param {String} authenticationToken
 * @param {ConcreteQuestionnaire} questionnaire
 * @param {String} name
 * @param {Boolean} randomizeQuestions
 *
 * @return {Future}
 * @resolve {ConcreteDimension}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function addConcreteDimension(
  authenticationToken,
  questionnaire,
  name,
  randomizeQuestions
) {
  return (
    fetchApi(questionnaire.href + "/concrete_dimension", {
      method: "POST",
      authenticationToken,
      body: JSON.stringify({ name }),
      language: questionnaire.languageData.currentLanguage
    })
      .chain(extractJson)
      .map(
        pipe(
          prop("dimension"),
          parseDimension
        )
      )
      // Update dimension with non-initial parameters after creation
      .chain(dimension =>
        updateDimension(
          authenticationToken,
          dimension,
          questionnaire.languageData.currentLanguage,
          { randomizeQuestions }
        )
      )
  );
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
 * @param authenticationToken
 * @param {ConcreteQuestionnaire} questionnaire
 * @param {ConcreteDimension} dimension
 *
 * @return {Future}
 * @resolve {ShadowDimension}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function addShadowDimension(authenticationToken, questionnaire, dimension) {
  return fetchApi(questionnaire.href + "/shadow_dimension", {
    method: "POST",
    authenticationToken,
    body: JSON.stringify({ id: dimension.id })
  })
    .chain(extractJson)
    .map(
      pipe(
        prop("dimension"),
        parseDimension
      )
    );
}

/**
 * Removes a Dimension from a ConcreteQuestionnaire and deletes it.
 *
 * The ConcreteQuestionnaire has to be updated or reloaded afterwards to reflect
 * the changes.
 *
 * @param authenticationToken
 * @param {ConcreteQuestionnaire} questionnaire
 * @param {Dimension} dimension
 *
 * @return {Future}
 * @resolve {Boolean} to true
 * @reject {TypeError|ApiError}
 * @cancel
 */
function removeDimension(authenticationToken, questionnaire, dimension) {
  if (contains(dimension, questionnaire.dimensions)) {
    return fetchApi(dimension.href, {
      method: "DELETE",
      authenticationToken
    }).map(() => true);
  } else {
    return Future.reject("Dimension not contained in Questionnaire.");
  }
}
export {
  createConcreteQuestionnaire,
  createShadowQuestionnaire,
  fetchMyQuestionnaires,
  fetchQuestionnaire,
  fetchQuestionnaireById,
  fetchQuestionnaireTemplates,
  fetchQuestionnaireForSubmissionById,
  updateQuestionnaire,
  deleteQuestionnaire,
  addConcreteDimension,
  addShadowDimension,
  removeDimension
};
