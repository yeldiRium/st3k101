import Vue from "vue";
import Vuex from "vuex-fluture";
import * as Future from "fluture/index.js";

import {
  initialize as initializeGlobalStore,
  store as global
} from "./modules/Global";
import {
  initialize as initializeLanguageStore,
  store as language
} from "./modules/Language";
import {
  initialize as initializeSessionStore,
  store as session
} from "./modules/Session";
import { store as questionnaires } from "./modules/Questionnaires";
import { store as dimensions } from "./modules/Dimensions";
import { store as questions } from "./modules/Questions";
import { store as trackerEntries } from "./modules/TrackerEntries";
import { store as submission } from "./modules/Submission";
import { store as statistics } from "./modules/Statistics";
import { store as response } from "./modules/Response";

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    initialLoading: "loading"
  },
  getters: {
    loading: state => {
      return state.initialLoading;
    }
  },
  mutations: {
    // eslint-disable-next-line no-unused-vars
    initialLoadingDone: (state, data) => {
      state.initialLoading = "done";
    },
    // eslint-disable-next-line no-unused-vars
    initialLoadingError: (state, error) => {
      state.initialLoading = "error";
    }
  },
  modules: {
    global,
    language,
    session,
    questionnaires,
    dimensions,
    questions,
    trackerEntries,
    submission,
    statistics,
    response
  }
});

export default store;

/**
 * Initializes all store modules in parallel.
 *
 * If any future fails, the rest will be cancelled.
 *
 * @returns a Future of all sub-futures.
 * @resolves with an array of all sub-futures' results. Probably an array of
 * many nothings.
 * @rejects with the error of the rejecting future.
 */
const initialize = function() {
  return Future.parallel(Infinity, [
    initializeGlobalStore(store, "global"),
    initializeLanguageStore(store, "language"),
    initializeSessionStore(store, "session")
  ]);
};

export { initialize };
