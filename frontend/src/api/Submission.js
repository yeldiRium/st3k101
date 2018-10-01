import * as R from "ramda";

import { fetchApi } from "./Util/Request";
import { extractJson } from "./Util/Response";

function submitResponse(
  submissionQuestionnaire,
  { email = null, password = null }
) {
  let dimensions = [];
  for (let dimension of submissionQuestionnaire.dimensions) {
    let questions = [];
    for (let question of dimension.questions) {
      questions.push({
        id: question.id,
        value: question.value
      });
    }
    dimensions.push({
      id: dimension.id,
      questions: questions
    });
  }

  let apiEndpoint = (submissionQuestionnaire.href + "/response").replace(
    "//",
    "/"
  );
  let payload = {
    captcha_token: "IAmNotARobot", // TODO
    dimensions: dimensions,
    data_subject: {
      email: email
    }
  };
  if (!R.isNil(password)) {
    payload["password"] = password;
  }

  return fetchApi(apiEndpoint, {
    method: "POST",
    body: JSON.stringify(payload)
  }).chain(extractJson);
}

function submitResponseLti(submissionQuestionnaire, authenticationToken) {
  let dimensions = [];
  for (let dimension of submissionQuestionnaire.dimensions) {
    let questions = [];
    for (let question of dimension.questions) {
      questions.push({
        id: question.id,
        value: question.value
      });
    }
    dimensions.push({
      id: dimension.id,
      questions: questions
    });
  }

  let apiEndpoint = (submissionQuestionnaire.href + "/lti/response").replace(
    "//",
    "/"
  );
  let payload = {
    captcha_token: "IAmNotARobot", // TODO
    dimensions: dimensions
  };

  return fetchApi(apiEndpoint, {
    method: "POST",
    body: JSON.stringify(payload),
    authenticationToken: authenticationToken
  }).chain(extractJson);
}

export { submitResponse, submitResponseLti };
