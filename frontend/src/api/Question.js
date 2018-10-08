import * as Future from "fluture/index.js";
import { assoc, dissoc, has, map, path, pipe, prop, when } from "ramda";

import { fetchApi } from "./Util/Request";
import { extractJson } from "./Util/Response";
import { parseQuestion } from "./Util/Parse";

import { ConcreteQuestion, ShadowQuestion } from "../model/SurveyBase/Question";
import renameProp from "./Util/renameProp";

/**
 * Fetches a Question by a given href in the given language.
 *
 * @param authenticationToken
 * @param {String} href
 * @param {Language} language
 *
 * @return {Future}
 * @resolve {Question}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function fetchQuestion(authenticationToken, href, language = null) {
  return fetchApi(href, {
    authenticationToken,
    language
  })
    .chain(extractJson)
    .map(parseQuestion);
}

/**
 * Fetches a Question by building its href from its id in the given language.
 *
 * @param authenticationToken
 * @param {String} id
 * @param {Language} language
 *
 * @return {Future}
 * @resolve {Question}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function fetchQuestionById(authenticationToken, id, language = null) {
  return fetchQuestion(authenticationToken, `/api/question/${id}`, language);
}

/**
 * Fetches a list of all available template Questions.
 *
 * @param authenticationToken
 * @param {Language} language on optional language in which the list should be
 *  retrieved
 * @returns {Future}
 * @resolve {Array<ConcreteQuestion>}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function fetchQuestionTemplates(authenticationToken, language = null) {
  return fetchApi("/api/question/template", {
    authenticationToken,
    language
  })
    .chain(extractJson)
    .map(map(parseQuestion));
}

/**
 * Updates the Question's fields. If a field is translatable, it is set
 * in the given language.
 *
 * @param authenticationToken
 * @param {Question} question
 * @param {Language} language
 * @param {Object} params
 *
 * @return {Future}
 * @resolve {Question}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function updateQuestion(authenticationToken, question, language, params) {
  let parsedParams = pipe(
    renameProp("referenceId", "reference_id"),
    when(
      has("range"),
      pipe(
        assoc("range_start", path(["range", "start"], params)),
        assoc("range_end", path(["range", "end"], params)),
        assoc("range_start_label", path(["range", "startLabel"], params)),
        assoc("range_end_label", path(["range", "endLabel"], params)),
        dissoc("range")
      )
    )
  )(params);

  return fetchApi(question.href, {
    method: "PATCH",
    authenticationToken,
    body: JSON.stringify(parsedParams),
    language
  })
    .chain(extractJson)
    .map(
      pipe(
        prop("question"),
        parseQuestion
      )
    );
}

export {
  fetchQuestion,
  fetchQuestionById,
  fetchQuestionTemplates,
  updateQuestion
};
