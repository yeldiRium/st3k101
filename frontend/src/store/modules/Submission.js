import {Future} from "fluture";

import {complement, equals, filter, find, isNil} from "ramda";

import {fetchQuestionnaireForSubmissionById} from "../../api/Questionnaire";

const store = {
    namespaced: true,
    state: {
        submissionQuestionnaires: [],
    },
    getters: {
        /**
         * Returns an initialized copy of the submissionQuestionnaire
         * for the given Questionnaire id, if it exists in the store.
         * @param state
         * @param getters
         * @param rootState
         * @param rootGetters
         */
        submissionQuestionnaireById(state, getters, rootState, rootGetters) {
            return (id) => {
                const submissionQuestionnaire = clone(find(
                    subQuest => subQuest.id === id,
                    state.submissionQuestionnaires
                ));

                if (isNil(submissionQuestionnaire)) {
                    return null;
                }

                return submissionQuestionnaire;
            };
        }
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
