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
    getters: {
        loading: (state, getters, rootState, rootGetters) => {
            // TODO: respect submodules' loading states
            return state.initialLoading;
        }
    },
    mutations: {
        initialLoadingDone: (state, data) => {
            state.initialLoading = "done";
        },
        initialLoadingError: (state, error) => {
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
