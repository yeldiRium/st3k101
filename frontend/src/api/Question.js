import * as Future from "fluture/index.js";
import {
  assoc,
  clone,
  contains,
  dissoc,
  has,
  map,
  path,
  pipe,
  prop,
  when
} from "ramda";

import { fetchApi } from "./Util/Request";
import { extractJson } from "./Util/Response";
import { parseQuestion } from "./Util/Parse";

import Question, {
  ConcreteQuestion,
  ShadowQuestion
} from "../model/SurveyBase/Question";
import renameProp from "./Util/renameProp";

const properties = ["text", "range"];

const concreteProperties = ["text"];

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

/**
 * Takes in a Question and populates its incoming references field by replacing
 * all resolvable References with their corresponding ShadowQuestion instances.
 *
 * Accesses the API to load the Questions.
 *
 * If this rejects, then some questions might be populated and some might still
 * be Resources. The exact state will have to be tested.
 *
 * @param authenticationToken
 * @param {ConcreteQuestion} concreteQuestion
 * @return {Future}
 * @resolve {Array<ShadowQuestion>}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function populateOwnedIncomingReferences(
  authenticationToken,
  concreteQuestion
) {
  const resolvedShadowQuestionFutures = [];

  // Use basic for loop to easily replace values.
  for (let i = 0; i < concreteQuestion.ownedIncomingReferences.length; i++) {
    /** @type {Resource|ShadowQuestion} */
    let reference = concreteQuestion.ownedIncomingReferences[i];

    if (instanceOf(reference, Resource)) {
      const shadowQuestionFuture = fetchQuestion(
        authenticationToken,
        reference.href,
        concreteQuestion.languageData.currentLanguage
      ).chain(shadowQuestion => {
        concreteQuestion.ownedIncomingReferences[i] = shadowQuestion;
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
 * @param authenticationToken
 * @param {ShadowQuestion} shadowQuestion
 * @return {Future}
 * @resolve {ConcreteQuestion}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function populateReferenceTo(authenticationToken, shadowQuestion) {
  if (instanceOf(shadowQuestion.referenceTo, Resource)) {
    const shadowQuestionFuture = fetchQuestion(
      authenticationToken,
      shadowQuestion.referenceTo.href,
      shadowQuestion.languageData.currentLanguage
    ).chain(concreteQuestion => {
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
 * @param authenticationToken
 * @param {Question} question
 * @return {Future}
 * @resolve {Array<ShadowQuestion>|ConcreteQuestion}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function populateQuestion(authenticationToken, question) {
  // Type warnings can be ignored, since they are tested.
  if (instanceOf(question, ShadowQuestion)) {
    return populateReferenceTo(authenticationToken, question);
  }
  if (instanceOf(question, ConcreteQuestion)) {
    return populateOwnedIncomingReferences(authenticationToken, question);
  }
}

export {
  fetchQuestion,
  fetchQuestionById,
  fetchQuestionTemplates,
  updateQuestion,
  populateOwnedIncomingReferences,
  populateReferenceTo,
  populateQuestion
};
