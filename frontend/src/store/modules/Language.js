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
        languageOptions: [],
        /**
         * TODO: this needs to be populated. Also find a middle ground between
         *       babel languages and available icons!
         * @type {Array.<string>} List of all languages in the system.
         */
        languages: []
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
            return Language.all()
                .mapRej(error => {
                    commit(
                        "setLoadingState", {
                            loadingState: "error",
                            error: error
                        }
                    );
                    return error;
                })
                .map(
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

                        return data;
                    }
                )
                .promise();
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
 * Since actions encase their return value in a resolved Promise (if the value
 * isn't a Promise itself), the Promise's resolving value has to be untangled.
 *
 * @param rootStore The instantiated store.
 * @param namespace The namespace in which this store resides.
 * @return a Future
 * @resolves with nothing.
 * @rejects with nothing.
 * @cancel doesn't exist.
 */
const initialize = function (rootStore, namespace) {
    return Future.tryP(
        () => rootStore.dispatch(`${namespace}/fetchLanguages`)
    );
};

export {
    store,
    initialize
}