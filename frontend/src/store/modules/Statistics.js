import { isNil, find, clone, reject, equals, without, concat } from "ramda";

import { Future } from "fluture/index.js";

import {
  fetchQuestionStatistic,
  fetchQuestionStatisticsByQuestionnaire
} from "../../api/Statistic";

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
    statisticByQuestionHref(state) {
      return href => {
        const statistic = clone(
          find(
            statistic => statistic.questionHref === href,
            state.questionStatistics
          )
        );

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
    fetchQuestionStatistic({ commit, rootGetters }, { question }) {
      return fetchQuestionStatistic(
        rootGetters["session/sessionToken"],
        question.href
      ).chain(statistic => {
        commit("patchQuestionStatisticInStore", { statistic });
        return Future.of(statistic);
      });
    },
    fetchQuestionStatisticsForQuestionnaire(
      { commit, rootGetters },
      { questionnaire }
    ) {
      return fetchQuestionStatisticsByQuestionnaire(
        rootGetters["session/sessionToken"],
        questionnaire.href
      ).chain(statistics => {
        commit("patchQuestionStatisticsInStore", { statistics });
        return Future.of(statistics);
      });
    }
  },
  mutations: {
    /**
     * Update currently stored representation of statistic in store
     * with provided value.
     *
     * Warning: Runs in O(n) time where n is the number of Questions
     * owned by the current DataClient. Use sparingly.
     *
     * @param state
     * @param statistic {QuestionStatistic}
     */
    patchQuestionStatisticInStore(state, { statistic }) {
      state.questionStatistics = reject(
        equals(statistic),
        state.questionStatistics
      ).concat([statistic]);
    },
    /**
     * Update all currently stored representations of statistics in store
     * with the statistics provided.
     *
     * Runs in O(n) time where n is the number of Questions owned by the
     * current DataClient.
     *
     * @param state
     * @param statistics {Array<QuestionStatistic>}
     */
    patchQuestionStatisticsInStore(state, { statistics }) {
      state.questionStatistics = concat(
        without(statistics, state.questionStatistics),
        statistics
      );
    }
  }
};

export default store;

export { store };
