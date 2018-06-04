import {__, allPass, has, map} from "ramda";
import Future from "fluture";

import Language from "../../api/Model/Language";

const store = {
    namespaced: true,
    state: {
        loading: {
            state: "loading",
            error: null
        },
        currentLanguage: {
            short: "de",
            long: "Deutsch"
        },
        languageOptions: []
    },
    getters: {
        loading: state => {
            return {
                loadingState: state.loading.state,
                error: state.loading.error
            };
        },
    },
    actions: {
        /**
         * Fetch the available Languages from the API and parse them to be
         * usable by the dropdown menu.
         */
        fetchLanguages({commit}) {
            return Language.all().fork(
                data => {
                    commit(
                        "setLoadingState", {
                            loadingState: "error",
                            error: error
                        }
                    );
                },
                data => {
                    data = map(
                        languageTuple => ({
                            short: languageTuple[0],
                            long: languageTuple[1]
                        }),
                        data
                    );
                    commit(
                        "setLoadingState", {
                            loadingState: "done"
                        }
                    );
                    commit("setLanguageOptions", data);
                }
            );
        }
    },
    mutations: {
        setLoadingState(state, {loadingState, error}) {
            state.loading.state = loadingState;
            state.loading.error = error;
        },
        setCurrentLanguage(state, language) {
            state.currentLanguage = language;
        },
        setLanguageOptions(state, languageOptions) {
            state.languageOptions = languageOptions;
        }
    }
};

export default store;

/**
 * Initializes this store's content.
 *
 * @param rootStore The instantiated store.
 * @param namespace The namespace in which this store resides.
 * @return a Future
 * @resolves with nothing.
 * @rejects with nothing.
 * @cancel doesn't exist.
 */
const initialize = function (rootStore, namespace) {
    return Future.tryP(() => rootStore.dispatch(`${namespace}/fetchLanguages`));
};

export {
    store,
    initialize
}