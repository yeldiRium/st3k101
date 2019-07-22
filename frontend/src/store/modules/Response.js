import * as api from "../../api/Response";
import { extractText } from "../../api/Util/Response";

const store = {
  namespaced: true,
  state: {},
  actions: {
    fetchQuestionnaireResponses(
      { rootGetters },
      { questionnaire, format = "json" }
    ) {
      const sessionToken = rootGetters["session/sessionToken"];
      return api
        .fetchQuestionnaireResponses(sessionToken, questionnaire, format)
        .chain(extractText);
    }
  }
};

export default store;

export { store };
