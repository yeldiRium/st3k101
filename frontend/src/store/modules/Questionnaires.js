import {
    __,
    always,
    any,
    assoc,
    bind,
    clone,
    contains,
    filter,
    find,
    isNil,
    keys,
    map,
    pipe,
    prop,
    propEq,
    reject,
    uniq,
    when,
    without
} from "ramda";
import Future from "fluture";

import {ConcreteQuestionnaire} from "../../model/SurveyBase/Questionnaire";
import {Language} from "../../model/Language";
import {
    addConcreteDimension,
    addShadowDimension,
    createConcreteQuestionnaire,
    createShadowQuestionnaire,
    deleteQuestionnaire,
    fetchMyQuestionnaires,
    fetchQuestionnaire,
    fetchQuestionnaireById,
    fetchQuestionnaireTemplates,
    removeDimension,
    updateQuestionnaire as apiUpdateQuestionnaire
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
                const questionnaires = pipe(
                    filter(
                        questionnaire => questionnaire.isOwnedBy(dataClient)
                    ),
                    map(clone)
                )(state.questionnaires);
                for (const questionnaire of questionnaires) {
                    questionnaire.dimensions = map(
                        rootGetters["dimensions/dimensionById"],
                        questionnaire.dimensions
                    );
                }
                return questionnaires;
            }
            return [];
        },
        questionnaireById(state, getters, rootState, rootGetters) {
            return function (id) {
                const questionnaire = clone(find(
                    questionnaire => questionnaire.id === id,
                    state.questionnaires
                ));

                if (isNil(questionnaire)) {
                    return null;
                }

                questionnaire.dimensions = map(
                    rootGetters["dimensions/dimensionById"],
                    questionnaire.dimensions
                );
                return questionnaire;
            }
        },
        questionnaireByHref(state, getters, rootState, rootGetters) {
            return function (href) {
                const questionnaire = clone(find(
                    questionnaire => questionnaire.href === href,
                    state.questionnaires
                ));

                if (isNil(questionnaire)) {
                    return null;
                }

                questionnaire.dimensions = map(
                    rootGetters["dimensions/dimensionByid"],
                    questionnaire.dimensions
                );
                return questionnaire;
            }
        },
        /**
         * Returns al Questionnaires that can be used as templates.
         *
         * @param state
         * @param getters
         * @param rootState
         * @param rootGetters
         * @returns {Array<ConcreteQuestionnaire>}
         */
        questionnaireTemplates(state, getters, rootState, rootGetters) {
            const questionnaires = pipe(
                filter(
                    questionnaire => questionnaire.template
                ),
                map(clone)
            )(state.questionnaires);
            for (const questionnaire of questionnaires) {
                questionnaire.dimensions = map(
                    rootGetters["dimensions/dimensionById"],
                    questionnaire.dimensions
                );
            }
            return questionnaires;
        }
    },
    actions: {
        /**
         * Check, if a Questionnaire with the given Questionnaire's id already
         * exists.
         * If so, overwrite the existing one.
         * Otherwise append the new one to the list.
         *
         * Also adds/overwrites all child Dimensions.
         *
         * Does so bottom up, so that hierarchies are never partially in the
         * store.
         *
         * @param dispatch
         * @param commit
         * @param {Questionnaire} questionnaire
         * @return {Future}
         * @resolve {Questionnaire}
         * @reject
         * @cancel
         */
        patchQuestionnaireInStore({dispatch, commit}, {questionnaire}) {
            const patchDimensionFutures = [];
            for (const dimension of questionnaire.dimensions) {
                patchDimensionFutures.push(
                    dispatch("dimensions/patchDimensionInStore",
                        {dimension},
                        {root: true}
                    )
                );
            }
            return Future.parallel(Infinity, patchDimensionFutures)
                .chain(() => {
                    commit("patchQuestionnaire", {questionnaire});
                    return Future.of(questionnaire);
                });
        },
        /**
         * Removes the given Questionnaire from the store.
         *
         * Ignored, if the Questionnaire is not found in the store.
         *
         * Also removes all child Dimensions from the store.
         *
         * @param commit
         * @param dispatch
         * @param {Questionnaire} questionnaire
         * @returns {Future}
         * @resolve {Boolean} to true
         * @reject
         * @cancel
         */
        removeQuestionnaireFromStore({commit, dispatch}, {questionnaire}) {
            return Future((reject, resolve) => {
                commit("removeQuestionnaire", {questionnaire});
                resolve(true);
            })
                .chain(() => {
                    const removeDimensionFutures = [];
                    for (const dimension of questionnaire.dimensions) {
                        removeDimensionFutures.push(
                            dispatch(
                                "dimensions/removeDimensionFromStore",
                                {dimension},
                                {root: true}
                            )
                        );
                    }
                    return Future.parallel(Infinity, removeDimensionFutures)
                        .map(() => true)
                });
        },
        /**
         * Create a new ConcreteQuestionnaire via the API and add it to the
         * store.
         *
         * @param dispatch
         * @param {Language} language
         * @param {String} name
         * @param {String} description
         * @param {Boolean} isPublic
         * @param {Boolean} allowEmbedded
         * @param {String} xapiTarget
         *
         * @return {Future}
         * @resolve {ConcreteQuestionnaire}
         * @reject {TypeError|ApiError}
         * @cancel
         */
        createConcreteQuestionnaire({dispatch, rootGetters}, {
            language,
            name,
            description,
            isPublic,
            allowEmbedded,
            xapiTarget
        }) {
            return createConcreteQuestionnaire(
                rootGetters["session/sessionToken"],
                language,
                name,
                description,
                isPublic,
                allowEmbedded,
                xapiTarget === "" ? null : xapiTarget
            )
                .chain(
                    questionnaire => dispatch(
                        "patchQuestionnaireInStore", {questionnaire}
                    )
                );
        },
        /**
         * Create a new ShadowQuestionnaire via the API and add it to the
         * store.
         *
         * @param dispatch
         * @param {ConcreteQuestionnaire} concreteQuestionnaire
         *
         * @return {Future}
         * @resolve {ShadowQuestionnaire}
         * @reject {TypeError|ApiError}
         * @cancel
         */
        createShadowQuestionnaire({dispatch, rootGetters}, {concreteQuestionnaire}) {
            return createShadowQuestionnaire(
                rootGetters["session/sessionToken"],
                concreteQuestionnaire)
                .chain(
                    shadowQuestionnaire => dispatch(
                        "patchQuestionnaireInStore",
                        {questionnaire: shadowQuestionnaire}
                    )
                );
        },
        /**
         * Loads all Questionnaires belonging to the current DataClient from the
         * API.
         *
         * @param dispatch
         * @param rootGetters
         * @returns {Future}
         * @resolves {Array<Questionnaire>}
         * @rejects with API error message
         * @cancel
         */
        loadMyQuestionnaires({dispatch, rootGetters}) {
            const dataClient = rootGetters["session/dataClient"];

            return fetchMyQuestionnaires(
                rootGetters["session/sessionToken"],
                dataClient.language
            )
                .chain(questionnaires => {
                    const patchQuestionnaireFutures = [];
                    for (const questionnaire of questionnaires) {
                        patchQuestionnaireFutures.push(
                            dispatch(
                                "patchQuestionnaireInStore",
                                {questionnaire}
                            )
                        );
                    }
                    return Future.parallel(Infinity, patchQuestionnaireFutures);
                });
        },
        /**
         * Fetches the Questionnaire in a certain Language via the API.
         * If the Questionnaire is already in the store, it will be
         * overwritten with the API result. Otherwise the Questionnaire is
         * added.
         *
         * At least one of href and id must be provided.
         *
         * @param dispatch
         * @param rootGetters
         * @param {String} href
         * @param {String} id
         * @param {Language} language
         *
         * @return {Future}
         * @resolve {Questionnaire} to true
         * @reject {TypeError|ApiError}
         * @cancel
         */
        fetchQuestionnaire(
            {dispatch, rootGetters},
            {href = null, id = null, language = null}
        ) {
            let future;
            if (isNil(href) && isNil(id)) {
                return Future.reject(
                    new BadRequestError("At least href or id has to be provided.")
                );
            }
            if (!isNil(href)) {
                future = fetchQuestionnaire(
                    authenticationToken,
                    href,
                    language
                );
            } else {
                future = fetchQuestionnaireById(
                    rootGetters["session/sessionToken"],
                    id,
                    language
                );
            }
            return future
                .chain(questionnaire => dispatch(
                    "patchQuestionnaireInStore",
                    {questionnaire}
                ));
        },
        /**
         * Fetches a list of all available template Questionnaires.
         *
         * @param dispatch
         * @param rootGetters
         * @param {Language} language on optional language in which the list should be
         *  retrieved
         * @returns {Future}
         * @resolve {Array<ConcreteQuestionnaire>}
         * @reject {TypeError|ApiError}
         * @cancel
         */
        fetchQuestionnaireTemplates({dispatch, rootGetters}, {language = null}) {
            return fetchQuestionnaireTemplates(
                rootGetters["session/sessionToken"],
                language
            )
                .chain(templates => {
                    const patchTemplateFutures = [];
                    for (const template of templates) {
                        patchTemplateFutures.push(dispatch(
                            "patchQuestionnaireInStore",
                            {questionnaire: template}
                        ));
                    }
                    return Future.parallel(Infinity, patchTemplateFutures);
                });
        },
        /**
         * Updates the given params on the Questionnaire and updates the
         * Questionnaire in the store. Translatable fields are set in the given
         * language or the Questionnaires current language.
         *
         * @param dispatch
         * @param rootGetters
         * @param {Questionnaire} questionnaire
         * @param {Language} language
         * @param {Object} params
         *
         * @return {Future}
         * @resolve {Questionnaire}
         * @reject {TypeError|ApiError}
         * @cancel
         */
        updateQuestionnaire(
            {dispatch, rootGetters},
            {questionnaire, language = null, params}
        ) {
            const correctLanguage = isNil(language)
                ? questionnaire.languageData.currentLanguage
                : language;

            return apiUpdateQuestionnaire(
                rootGetters["session/sessionToken"],
                questionnaire,
                correctLanguage,
                params
            )
                .chain(result => dispatch(
                    "patchQuestionnaireInStore",
                    {questionnaire: result}
                ));
        },
        /**
         * Replaces the old Challenge of the given kind with a new one on a gi-
         * ven Questionnaire.
         *
         * TODO: set via API
         *
         * @param dispatch
         * @param rootGetters
         * @param {Questionnaire} questionnaire
         * @param {Challenge} challenge
         *
         * @return {Future}
         * @resolve {Questionnaire}
         * @reject {TypeError|ApiError}
         * @cancel
         */
        updateChallengeOnQuestionnaire(
            {dispatch, rootGetters},
            {questionnaire, challenge}
        ) {
            let data = {};

            switch (challenge.name) {
                case "EMailWhitelist":
                    data["email_whitelist"] = challenge.emails;
                    data["email_whitelist_enabled"] = challenge.isEnabled;
                    break;
                case "EMailBlacklist":
                    data["email_blacklist"] = challenge.emails;
                    data["email_blacklist_enabled"] = challenge.isEnabled;
                    break;
                case "Password":
                    data["password"] = challenge.password;
                    data["password_enabled"] = challenge.isEnabled;
                    break;
                default:
                    return Future.reject(
                        new BadRequestError("Challenge's name is invalid.")
                    );
            }

            return apiUpdateQuestionnaire(
                rootGetters["session/sessionToken"],
                questionnaire,
                questionnaire.languageData.currentLanguage,
                data
            )
                .chain(result => dispatch(
                    "patchQuestionnaireInStore",
                    {questionnaire: result}
                ));
        },
        /**
         * Deletes the given Questionnaire via the API and removes it from the
         * store.
         *
         * @param dispatch
         * @param rootGetters
         * @param {Questionnaire} questionnaire
         *
         * @return {Future}
         * @resolve {Boolean} with true
         * @reject see API
         * @cancel
         */
        deleteQuestionnaire({dispatch, rootGetters}, {questionnaire}) {
            return deleteQuestionnaire(
                rootGetters["session/sessionToken"],
                questionnaire
            )
                .chain(() => dispatch(
                    "removeQuestionnaireFromStore",
                    {questionnaire}
                ))
                // TODO: remove this
                // Remove the questionnaire even if the API throws an error.
                // This is used for testing while the API is not ready yet.
                .chainRej(error => {
                    return dispatch(
                        "removeQuestionnaireFromStore",
                        {questionnaire}
                    )
                        .chain(() => Future.reject(error));
                })
        },
        /**
         * Add a new ConcreteDimension to the ConcreteQuestionnaire.
         *
         * @param commit
         * @param dispatch
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
        addConcreteDimension({commit, dispatch, rootGetters},
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
                rootGetters["session/sessionToken"],
                questionnaire,
                name,
                randomizeQuestions
            )
                .chain(concreteDimension => {
                    commit("addDimensionToQuestionnaire", {
                        questionnaire,
                        dimension: concreteDimension
                    });
                    return dispatch(
                        "dimensions/patchDimensionInStore",
                        {dimension: concreteDimension},
                        {root: true}
                    );
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
                rootGetters["session/sessionToken"],
                questionnaire,
                concreteDimension
            )
                .chain(shadowDimension => {
                    commit("addDimensionToQuestionnaire", {
                        questionnaire,
                        dimension: shadowDimension
                    });
                    return dispatch(
                        "dimensions/patchDimensionInStore",
                        {dimension: shadowDimension},
                        {root: true}
                    )
                    // Reload original ConcreteDimension to have an accurate
                    // reference count
                        .chain(() => dispatch(
                            "dimensions/fetchDimension",
                            {
                                href: concreteDimension.href,
                                language: concreteDimension.languageData.currentLanguage
                            }
                        ))
                        // still resolve to the new ShadowDimension
                        .map(() => shadowDimension);
                })
        },
        /**
         * Removes a Dimension from a ConcreteQuestionnaire.
         *
         * @param commit
         * @param dispatch
         * @param rootGetters
         * @param {ConcreteQuestionnaire} questionnaire
         * @param {Dimension} dimension
         *
         * @return {Future}
         * @resolve {ConcreteQuestionnaire}
         * @reject {TypeError|ApiError}
         * @cancel
         */
        removeDimension(
            {commit, dispatch, rootGetters},
            {questionnaire, dimension}
        ) {
            if (questionnaire.isShadow) {
                return Future.reject(
                    new ValidationError(
                        "RemoveDimension may not be called on ShadowQuestionnaire.",
                        {}
                    )
                );
            }

            return removeDimension(
                rootGetters["session/sessionToken"],
                questionnaire,
                dimension
            )
                .chain(() => {
                    commit(
                        "removeDimensionFromQuestionnaire",
                        {
                            questionnaire,
                            dimension
                        }
                    );
                    return dispatch(
                        "dimensions/removeDimensionFromStore",
                        {dimension},
                        {root: true}
                    );
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
            questionnaire.dimensions = map(
                dimension => dimension.id,
                questionnaire.dimensions
            );

            let existingQuestionnaireWasReplaced = false;
            state.questionnaires = map(
                iQuestionnaire => {
                    if (questionnaire.identifiesWith(iQuestionnaire)) {
                        if (!questionnaire.isReadonlyTemplate || iQuestionnaire.isReadonlyTemplate) {
                            existingQuestionnaireWasReplaced = true;
                            return questionnaire;
                        }
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
            const questionnaireInStore = find(
                bind(questionnaire.identifiesWith, questionnaire),
                state.questionnaires
            );

            if (!isNil(questionnaireInStore)) {
                questionnaireInStore.dimensions.push(dimension.id);
                questionnaireInStore.dimensions =
                    uniq(questionnaireInStore.dimensions);
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
            const questionnaireInStore = find(
                bind(questionnaire.identifiesWith, questionnaire),
                state.questionnaires
            );

            if (!isNil(questionnaireInStore)) {
                questionnaireInStore.dimensions = without(
                    [dimension.id],
                    questionnaireInStore.dimensions
                );
            }
        }
    }
};

export default store;

export {
    store
};
