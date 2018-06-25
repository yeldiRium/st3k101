import {
    __,
    any,
    bind,
    contains,
    filter,
    find,
    isNil,
    keys,
    map,
    prop,
    reject
} from "ramda";
import Future from "fluture";

import {ConcreteQuestionnaire} from "../../model/SurveyBase/Questionnaire";
import {Language} from "../../model/Language";
import {
    addConcreteDimension,
    addShadowDimension,
    createConcreteQuestionnaire,
    deleteQuestionnaire, fetchMyQuestionnaires,
    fetchQuestionnaire, fetchQuestionnaireById,
    removeDimension,
    updateQuestionnaire
} from "../../api/Questionnaire";
import {BadRequestError} from "../../api/Errors";

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
        },
        questionnaireById(state) {
            return id => find(
                questionnaire => questionnaire.id === id,
                state.questionnaires
            )
        },
        questionnaireByHref(state) {
            return href => find(
                questionnaire => questionnaire.href === href,
                state.questionnaires
            )
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
         */
        loadMyQuestionnaires({commit, dispatch, getters, rootGetters}) {
            const dataClient = rootGetters["session/dataClient"];

            return fetchMyQuestionnaires(dataClient.language)
                .chain(questionnaires => {
                    for (const questionnaire of questionnaires) {
                        commit("patchQuestionnaire", {questionnaire});
                    }
                    return Future.of(true);
                });
        },
        /**
         * Create a new ConcreteQuestionnaire via the API and add it to the
         * store.
         *
         * @param commit
         * // TODO: is owner parameter necessary?
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
        // TODO: createShadowQuestionnaire
        /**
         * Fetches the Questionnaire in a certain Language via the API.
         * If the Questionnaire is already in the store, it will be
         * overwritten with the API result. Otherwise the Questionnaire is
         * added.
         *
         * At least one of href and id must be provided.
         *
         * @param commit
         * @param {String} href
         * @param {String} id
         * @param {Language} language
         *
         * @return {Future}
         * @resolve {Questionnaire} to true
         * @reject {TypeError|ApiError}
         * @cancel
         */
        fetchQuestionnaire({commit}, {href = null, id = null, language = null}) {
            let future;
            if (isNil(href) && isNil(id)) {
                return Future.reject(
                    new BadRequestError("At least href or id has to be provided.")
                );
            }
            if (!isNil(href)) {
                future = fetchQuestionnaire(href, language);
            } else {
                future = fetchQuestionnaireById(id, language);
            }
            return future
                .chain(questionnaire => {
                    commit("patchQuestionnaire", {questionnaire});

                    // MAYBE: refactor this, so that only dimensions have
                    // to be added. could do this in a separate action and have
                    // an action on Dimension store, which adds the Questions.
                    for (const dimension of questionnaire.dimensions) {
                        commit(
                            "dimensions/patchDimension",
                            {dimension},
                            {root: true}
                        );
                        for (const question of dimension.questions) {
                            commit(
                                "questions/patchQuestion",
                                {question},
                                {root: true}
                            );
                        }
                    }
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

                    for (const dimension of questionnaire.dimensions) {
                        for (const question of dimension.questions) {
                            commit(
                                "questions/removeQuestion",
                                {question},
                                {root: true}
                            );
                        }
                        commit(
                            "dimensions/removeDimension",
                            {dimension},
                            {root: true}
                        );
                    }
                    return Future.of(true);
                })
                // TODO: remove this
                // Remove the questionnaire even if the API throws an error.
                // This is used for testing while the API is not ready yet.
                .chainRej(error => {
                    commit("removeQuestionnaire", {questionnaire});

                    for (const dimension of questionnaire.dimensions) {
                        for (const question of dimension.questions) {
                            commit(
                                "questions/removeQuestion",
                                {question},
                                {root: true}
                            );
                        }
                        commit(
                            "dimensions/removeDimension",
                            {dimension},
                            {root: true}
                        );
                    }
                    return Future.reject(error);
                });
        },
        /**
         * Add a new ConcreteDimension to the ConcreteQuestionnaire.
         *
         * @param commit
         * @param rootGetters
         * @param {ConcreteQuestionnaire} questionnaire
         * @param {String} name
         * @param {Boolean} randomizeQuestions
         *
         * @return {Future}
         * @resolve {ConcreteDimension}
         * @reject {TypeError|ApiError}
         * @cancel
         */
        addConcreteDimension({commit, rootGetters},
                             {
                                 questionnaire,
                                 params: {name, randomizeQuestions}
                             }) {
            if (questionnaire.isShadow) {
                return Future.reject(
                    new ValidationError(
                        "AddConcreteDimension may not be called on ShadowQuestionnaire.",
                        {}
                    )
                );
            }

            return addConcreteDimension(
                questionnaire,
                rootGetters["session/dataClient"],
                name,
                randomizeQuestions
            ).chain(concreteDimension => {
                commit("addDimensionToQuestionnaire", {
                    questionnaire,
                    dimension: concreteDimension
                });
                commit(
                    "dimensions/patchDimension",
                    {dimension: concreteDimension},
                    {root: true}
                );
                return Future.of(concreteDimension);
            })
        },
        /**
         * Add a new ShadowDimension to the ConcreteQuestionnaire referencing
         * the given ConcreteDimension.
         *
         * @param commit
         * @param dispatch
         * @param rootGetters
         * @param {ConcreteQuestionnaire} questionnaire
         * @param {ConcreteDimension} concreteDimension
         *
         * @return {Future}
         * @resolve {ShadowDimension}
         * @reject {TypeError|ApiError}
         * @cancel
         */
        addShadowDimension({commit, dispatch, rootGetters},
                           {
                               questionnaire,
                               concreteDimension
                           }) {
            if (questionnaire.isShadow) {
                return Future.reject(
                    new ValidationError(
                        "AddShadowDimension may not be called on ShadowQuestionnaire.",
                        {}
                    )
                );
            }
            if (concreteDimension.isShadow) {
                return Future.reject(
                    new ValidationError(
                        "AddShadowDimension may not be called for ShadowDimension.",
                        {}
                    )
                );
            }

            return addShadowDimension(
                questionnaire,
                rootGetters["session/dataClient"],
                concreteDimension
            ).chain(shadowDimension => {
                commit("addDimensionToQuestionnaire", {
                    questionnaire,
                    dimension: shadowDimension
                });
                // Add new ShadowDimension to Dimension store
                commit(
                    "dimensions/patchDimension",
                    {dimension: shadowDimension},
                    {root: true}
                );
                // Add ShadowQuestions created on the server to Question store
                for (const shadowQuestion of shadowDimension.questions) {
                    commit(
                        "questions/patchQuestion",
                        {question: shadowQuestion},
                        {root: true}
                    );
                }
                // Reload original ConcreteDimension to have an accurate
                // reference count
                return dispatch(
                    "dimensions/fetchDimension",
                    {
                        href: concreteDimension.href,
                        language: concreteDimension.languageData.currentLanguage
                    }
                    // still resolve to the new ShadowDimension
                ).map(() => shadowDimension);
            })
        },
        /**
         * Removes a Dimension from a ConcreteQuestionnaire.
         *
         * @param commit
         * @param {ConcreteQuestionnaire} questionnaire
         * @param {Dimension} dimension
         *
         * @return {Future}
         * @resolve {ConcreteQuestionnaire}
         * @reject {TypeError|ApiError}
         * @cancel
         */
        removeDimension({commit}, {questionnaire, dimension}) {
            if (questionnaire.isShadow) {
                return Future.reject(
                    new ValidationError(
                        "RemoveDimension may not be called on ShadowQuestionnaire.",
                        {}
                    )
                );
            }

            return removeDimension(questionnaire, dimension)
                .chain(() => {
                    commit(
                        "removeDimensionFromQuestionnaire",
                        {
                            questionnaire,
                            dimension
                        }
                    );

                    for (const question of dimension.questions) {
                        commit(
                            "questions/removeQuestion",
                            {question},
                            {root: true}
                        );
                    }
                    commit(
                        "dimensions/removeDimension",
                        {dimension},
                        {root: true}
                    );
                    return Future.of(questionnaire);
                })
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
        },
        /**
         * Adds a Dimension to a ConcreteQuestionnaire.
         * Overwrites an existing Dimension, if one with the same id exists.
         *
         * @param state
         * @param {ConcreteQuestionnaire} questionnaire
         * @param {Dimension} dimension
         */
        addDimensionToQuestionnaire(state, {questionnaire, dimension}) {
            if (!isNil(questionnaire)) {
                let existingDimensionWasReplaced = false;
                questionnaire.dimensions = map(
                    iDimension => {
                        if (dimension.identifiesWith(iDimension)) {
                            existingDimensionWasReplaced = true;
                            return dimension;
                        }
                        return iDimension;
                    },
                    questionnaire.dimensions
                );
                if (existingDimensionWasReplaced) {
                    return;
                }

                questionnaire.dimensions.push(dimension);
            }
        },
        /**
         * Removes a Dimension from a ConcreteQuestionnaire.
         * Does nothing, if the Dimension isn't found.
         *
         * @param state
         * @param {ConcreteQuestionnaire} questionnaire
         * @param {Dimension} dimension
         */
        removeDimensionFromQuestionnaire(state, {questionnaire, dimension}) {
            if (!isNil(questionnaire)) {
                questionnaire.dimensions = reject(
                    iDimension => iDimension.id === dimension.id,
                    questionnaire.dimensions
                );
            }
        }
    }
};

export default store;

export {
    store
};
