import { fetchApi } from "./Util/Request";

function fetchQuestionnaireResponses(
  authenticationToken,
  questionnaire,
  format = "json"
) {
  let apiEndpoint = (questionnaire.href + "/response").replace("//", "/");
  return fetchApi(apiEndpoint, {
    authenticationToken,
    query: { format }
  });
}

export { fetchQuestionnaireResponses };
