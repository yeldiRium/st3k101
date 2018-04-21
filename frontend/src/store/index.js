import Vue from "vue";
import Vuex from "vuex";
import Future from "fluture";

import {store as language, initialize as initializeLanguageStore} from "./modules/Language";
import {store as session} from "./modules/Session";

Vue.use(Vuex);

const store = new Vuex.Store({
    state: {
        initialLoading: "loading"
    },
    mutations: {
        initialLoadingDone: function(state, data) {
            state.initialLoading = "done";
        },
        initialLoadingError: function(state, error) {
            state.initialLoading = "error";
        }
    },
    modules: {
        language,
        session
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
const initialize = function () {
    return Future.parallel(Infinity, [
        initializeLanguageStore(store, "language")
    ]);
};

export {
    initialize
};
