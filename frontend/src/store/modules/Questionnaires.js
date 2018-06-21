import {
    __,
    any,
    bind,
    contains,
    filter,
    isNil,
    keys,
    map,
    prop,
    reject
} from "ramda";
import Future from "fluture";

import {ConcreteQuestionnaire} from "../../model/SurveyBase/Questionnaire";
import {Language, LanguageData} from "../../model/Language";
import {
    createConcreteQuestionnaire,
    deleteQuestionnaire,
    fetchQuestionnaire,
    updateQuestionnaire
} from "../../api/Questionnaire";

const store = {
    namespaced: true,
    state: {
        /**
         * All Questionnaires that have been loaded from the API.
         *
         * @type {Array<Questionnaire>}
         */
        questionnaires: []
    },
    getters: {
        /**
         * All Questionnaires that belong to the current DataClient.
         *
         * @return {Array<Questionnaire>}
         */
        myQuestionnaires(state, getters, rootState, rootGetters) {
            const dataClient = rootGetters["session/dataClient"];

            if (!isNil(dataClient)) {
                return filter(
                    questionnaire => questionnaire.isOwnedBy(dataClient),
                    state.questionnaires
                );
            }
            return [];
        }
    },
    actions: {
        /**
         * Loads all Questionnaires belonging to the current DataClient from the
         * API.
         *
         * @param context
         * @returns {Future}
         * @resolves with nothing
         * @rejects with API error message
         * @cancel
         *
         * TODO: implement this and remove test data.
         */
        loadMyQuestionnaires({commit, rootGetters}) {
            return Future((reject, resolve) => {
                const dataClient = rootGetters["session/dataClient"];

                const en = new Language("en", "English");
                const languageData = new LanguageData(en, en, [en]);

                const testQuestionnaires = [
                    new ConcreteQuestionnaire("http://blubblab/api/questionnaire/1", "1", dataClient, languageData, "Dieser ConcreteQuestionnaire gehört mir.", "Ein schöner Questionnaire, nicht wahr? Dies ist seine Beschreibung.", true, true, "i don't even know, what this is", [], 0, []),
                    new ConcreteQuestionnaire("http://blubblab/api/questionnaire/2", "2", dataClient, languageData, "Dieser ShadowQuestionnaire gehört mir.", "Ein schöner Questionnaire, nicht wahr? Dies ist seine Beschreibung.", false, true, "i don't even know, what this is", [], 0, [])
                ];

                for (const questionnaire of testQuestionnaires) {
                    commit("patchQuestionnaire", {questionnaire});
                }

                resolve();
            });
        },
        /**
         * Create a new ConcreteQuestionnaire via the API and add it to the
         * store.
         *
         * @param commit
         * @param {DataClient} dataClient
         * @param {Language} language
         * @param {String} name
         * @param {String} description
         * @param {Boolean} isPublic
         * @param {Boolean} allowEmbedded
         * @param {String} xapiTarget
         *
         * @return {Future}
         * @resolve see API
         * @reject see API
         * @cancel
         */
        createConcreteQuestionnaire({commit}, {
            dataClient,
            language,
            name,
            description,
            isPublic,
            allowEmbedded,
            xapiTarget
        }) {
            return createConcreteQuestionnaire(
                dataClient,
                language,
                name,
                description,
                isPublic,
                allowEmbedded,
                xapiTarget
            ).chain(
                questionnaire => {
                    commit("patchQuestionnaire", {questionnaire});
                    return Future.of(questionnaire);
                }
            )
        },
        /**
         * Fetches the Questionnaire in a certain Language via the API.
         * If the Questionnaire is already in the store, it will be
         * overwritten with the API result. Otherwise the Questionnaire is
         * added.
         *
         * @param commit
         * @param {String} href
         * @param {Language} language
         *
         * @return {Future}
         * @resolve {Questionnaire} to true
         * @reject with an API error message
         * @cancel
         */
        fetchQuestionnaire({commit}, {href, language}) {
            return fetchQuestionnaire(href, language)
                .chain(questionnaire => {
                    commit("patchQuestionnaire", {questionnaire});
                    return Future.of(questionnaire);
                })
        },
        /**
         * Updates the given params on the Questionnaire and updates the
         * Questionnaire in the store. Translatable fields are set in the given
         * language or the Questionnaires current language.
         *
         * @param commit
         * @param {Questionnaire} questionnaire
         * @param {Language} language
         * @param {Object} params
         *
         * @return {Future}
         * @resolve {Questionnaire}
         * @reject {TypeError|ApiError}
         * @cancel
         */
        updateQuestionnaire({commit}, {questionnaire, language = null, params}) {
            const correctLanguage = isNil(language)
                ? questionnaire.languageData.currentLanguage
                : language;

            return updateQuestionnaire(questionnaire, correctLanguage, params)
                .chain(result => {
                    commit("patchQuestionnaire", {questionnaire: result});
                    return Future.of(result);
                })
                // TODO: remove this
                // Patches the questionnaire manually and incredibly stupidly
                // just so that the app seems to work without the api.
                .chainRej(error => {
                    for (const key in params) {
                        if (!isNil(questionnaire[key])) {
                            questionnaire[key] = params[key];
                        }
                    }
                    // This commit isn't technically necessary, since the object
                    // is mutated directly above, but it let's us use the
                    // devtools while playing around without api.
                    commit("patchQuestionnaire", {questionnaire});
                    // This prevents us from seeing any errors.
                    return Future.of(questionnaire);
                });
        },
        /**
         * Deletes the given Questionnaire via the API and removes it from the
         * store.
         *
         * @param commit
         * @param {Questionnaire} questionnaire
         *
         * @return {Future}
         * @resolve {Boolean} with true
         * @reject see API
         * @cancel
         */
        deleteQuestionnaire({commit}, {questionnaire}) {
            return deleteQuestionnaire(questionnaire)
                .chain(() => {
                    commit("removeQuestionnaire", {questionnaire});
                    return Future.of(true);
                })
                // TODO: remove this
                // Remove the questionnaire even if the API throws an error.
                // This is used for testing while the API is not ready yet.
                .chainRej(error => {
                    commit("removeQuestionnaire", {questionnaire});
                    return Future.reject(error);
                });
        }
    },
    mutations: {
        /**
         * Check, if a Questionnaire with the given Questionnaire's id already
         * exists.
         * If so, overwrite the existing one.
         * Otherwise append the new one to the list.
         *
         * @param state
         * @param {Questionnaire} questionnaire
         */
        patchQuestionnaire(state, {questionnaire}) {
            let existingQuestionnaireWasReplaced = false;
            state.questionnaires = map(
                iQuestionnaire => {
                    if (questionnaire.identifiesWith(iQuestionnaire)) {
                        existingQuestionnaireWasReplaced = true;
                        return questionnaire;
                    }
                    return iQuestionnaire;
                },
                state.questionnaires
            );
            if (existingQuestionnaireWasReplaced) {
                return;
            }

            state.questionnaires.push(questionnaire);
        },
        /**
         * Removes the given Questionnaire from the store.
         *
         * Ignored, if the Questionnaire is not found in the store.
         *
         * @param state
         * @param {Questionnaire} questionnaire
         */
        removeQuestionnaire(state, {questionnaire}) {
            state.questionnaires = reject(
                bind(questionnaire.identifiesWith, questionnaire),
                state.questionnaires
            );
        }
    }
};

export default store;

export {
    store
};
