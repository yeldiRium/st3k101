import {__, allPass, has, map} from "ramda";
import Future from "fluture";

import Language from "../../api/Model/Language";

const store = {
    namespaced: true,
    state: {
        loading: "loading",
        currentLanguage: {
            short: "de",
            long: "Deutsch"
        },
        languageOptions: []
    },
    actions: {
        /**
         * Fetch the available Languages from the API and parse them to be
         * usable by the dropdown menu.
         */
        fetchLanguages({commit}) {
            return Language.all().fork(
                data => {
                    commit("setLoadingState", "error");
                },
                data => {
                    data = map(
                        languageTuple => ({
                            short: languageTuple[0],
                            long: languageTuple[1]
                        }),
                        data
                    );
                    commit("setLoadingState", "done");
                    commit("setLanguageOptions", data);
                }
            );
        }
    },
    mutations: {
        setLoadingState(state, loadingState) {
            state.loading = loadingState;
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