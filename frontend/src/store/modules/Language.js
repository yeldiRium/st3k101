import {__, allPass, has, map} from "ramda";

import Language from "../../model/Language";

const store = {
    namespaced: true,
    state: {
        currentLanguage: {
            short: "de",
            long: "Deutsch"
        },
        languageOptions: [],
        /**
         * TODO: this needs to be populated.
         * @type {Array.<Language>} List of all languages in the system.
         */
        languages: [
            new Language("de", "German"),
            new Language("en", "English"),
            new Language("it", "Italian"),
            new Language("es", "Spanish"),
            new Language("ch", "Chinese")
        ]
    },
    actions: {
        /**
         * TODO:
         * Fetch the available Languages from the API and parse them to be
         * usable by the dropdown menu.
         */
        fetchLanguages({commit}) {
            return [];
        }
    },
    mutations: {
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
    return rootStore.dispatch(`${namespace}/fetchLanguages`);
};

export {
    store,
    initialize
}
