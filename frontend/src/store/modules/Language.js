import {__, allPass, ascend, has, map, prop, sort} from "ramda";
import Future from "fluture";

import Language from "../../model/Language";
import {fetchLanguages} from "../../api/Language";

const byShortName = ascend(prop("shortName"));

const store = {
    namespaced: true,
    state: {
        currentLanguage: {
            short: "de",
            long: "Deutsch"
        },
        /**
         * @type {Array<Language>} List of all languages in the system.
         */
        languages: null
    },
    actions: {
        /**
         * Fetches the available Languages on the server.
         *
         * @returns {Future}
         * @resolve {Array<Language>}
         * @reject {TypeError|ApiError}
         * @cancel
         */
        fetchLanguages({commit}) {
            return fetchLanguages()
                .chain(languages => {
                    const sortedLanguages = sort(byShortName, languages);
                    commit("setLanguages", sortedLanguages);
                    return Future.of(sortedLanguages);
                });
        }
    },
    mutations: {
        setCurrentLanguage(state, language) {
            state.currentLanguage = language;
        },
        /**
         * @param state
         * @param {Array<Language>} languages
         */
        setLanguages(state, languages) {
            state.languages = languages;
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
    return rootStore.dispatch(`${namespace}/fetchLanguages`);
};

export {
    store,
    initialize,
    byShortName
}
