import { Future } from "fluture/index.js";

import { complement, equals, filter, find, isNil } from "ramda";

import { fetchQuestionnaireForSubmissionById } from "../../api/Questionnaire";

const store = {
  namespaced: true,
  state: {
    submissionQuestionnaires: []
  },
  actions: {
    fetchSubmissionQuestionnaireById(
      { commit, rootGetters },
      { id, language }
    ) {
      return fetchQuestionnaireForSubmissionById(
        rootGetters["session/sessionToken"],
        id,
        language
      ).chain(questionnaire => {
        commit("patchSubmissionQuestionnaireInStore", { questionnaire });
        return Future.of(questionnaire);
      });
    }
  },
  mutations: {
    patchSubmissionQuestionnaireInStore(state, { questionnaire }) {
      state.submissionQuestionnaires = filter(
        complement(equals(questionnaire)),
        state.submissionQuestionnaires
      );
      state.submissionQuestionnaires.push(questionnaire.clone());
    }
  }
};

export default store;

export { store };
