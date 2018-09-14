import {isNil, find, clone, reject, equals} from "ramda";

import {Future} from "fluture";

import QuestionStatistic from "../../model/Statistic/QuestionStatistic";
import {fetchQuestionStatistic, fetchQuestionStatisticsByQuestionnaire} from "../../api/Statistic";

const store = {
    namespaced: true,
    state: {
        /***
         * All QuestionStatistics objects that have been loaded from the API.
         *
         * @type {Array<QuestionStatistic>}
         */
        questionStatistics: []
    },
    getters: {
        statisticByQuestionHref(state, getters, rootState, rootGetters) {
            return (href) => {
                const statistic = clone(find(
                    statistic => statistic.questionHref === href,
                    state.questionStatistics
                ));

                if (isNil(statistic)) {
                    return null;
                }

                return statistic;
            };
        }
    },
    actions: {
        /***
         * Fetches the QuestionStatistic object for a given question
         * via the api and stores it.
         *
         * @param commit
         * @param rootGetters
         * @param question {Question}
         */
        fetchQuestionStatistic({commit, rootGetters}, {question}) {
            return fetchQuestionStatistic(
                rootGetters["session/sessionToken"],
                question.href
            )
                .chain(statistic => {
                        commit(
                            "patchQuestionStatisticInStore",
                            {statistic}
                        );
                        return Future.of(statistic);
                    }
                );
        },
        fetchQuestionStatisticsForQuestionnaire({commit, rootGetters}, {questionnaire}) {
           return fetchQuestionStatisticsByQuestionnaire(
               rootGetters["session/sessionToken"],
               questionnaire.href
           )
               .chain(statistics => {
                   for (let statistic of statistics) {
                       commit(
                           "patchQuestionStatisticInStore",
                           {statistic}
                       )
                   }
                   return Future.of(statistics);
               });
        }
    },
    mutations: {
        /**
         * Update currently stored representation of statistic in store
         * with provided value.
         *
         * @param state
         * @param statistic {QuestionStatistic}
         */
        patchQuestionStatisticInStore(state, {statistic}) {
            state.questionStatistics = reject(
                equals(statistic),
                state.questionStatistics
            ).concat([statistic]);
        }
    }
};

export default store;

export {
    store
};