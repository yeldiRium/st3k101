import {Future} from "fluture";

import {complement, equals, filter, find, isNil} from "ramda";

import {fetchQuestionnaireForSubmissionById} from "../../api/Questionnaire";

const store = {
    namespaced: true,
    state: {
        submissionQuestionnaires: [],
    },
    actions: {
        fetchSubmissionQuestionnaireById({commit}, {id, language}) {
            return fetchQuestionnaireForSubmissionById(id, language)
                .chain(questionnaire => {
                    commit("patchSubmissionQuestionnaireInStore", {questionnaire});
                    return Future.of(questionnaire);
                })
        }
    },
    mutations: {
        patchSubmissionQuestionnaireInStore(state, {questionnaire}) {
            state.submissionQuestionnaires = filter(
                complement(equals(questionnaire)),
                state.submissionQuestionnaires
            );
            state.submissionQuestionnaires.push(questionnaire.clone());
        }
    }
};

export default store;

export {store};
