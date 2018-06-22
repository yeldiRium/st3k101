import {bind, find, isNil, map, reject} from "ramda";
import Future from "fluture";

import {
    addConcreteQuestion,
    addShadowQuestion,
    fetchDimension,
    removeQuestion,
    updateDimension
} from "../../api/Dimension";

const store = {
    namespaced: true,
    state: {
        /**
         * All Dimensions that have been loaded from the API.
         *
         * @type {Array<Dimension>}
         */
        dimensions: []
    },
    getters: {
        dimensionById(state) {
            return id => {
                find(
                    dimension => dimension.id === id,
                    state.dimensions
                )
            }
        },
        dimensionByHref(state) {
            return href => {
                find(
                    dimension => dimension.href === href,
                    state.dimensions
                )
            }
        }
    },
    actions: {
        /**
         * Fetches the Dimension in a certain Language via the API.
         * If the Dimension is already in the store, it will be
         * overwritten with the API result. Otherwise the Dimension is
         * added.
         *
         * @param commit
         * @param {String} href
         * @param {Language} language
         *
         * @return {Future}
         * @resolve {Dimension} to true
         * @reject {TypeError|ApiError}
         * @cancel
         */
        fetchDimension({commit}, {href, language}) {
            return fetchDimension(href, language)
                .chain(dimension => {
                    commit("patchDimension", {dimension});
                    // Add each Question to Question store for direct lookup
                    for (const question of dimension.questions) {
                        commit(
                            "questions/patchQuestion",
                            {question},
                            {root: true}
                        );
                    }
                    return Future.of(dimension);
                });
        },
        /**
         * Updates the given params on the Dimension and updates the
         * Dimension in the store. Translatable fields are set in the given
         * language or the Dimensions current language.
         *
         * @param commit
         * @param {Dimension} dimension
         * @param {Language} language
         * @param {Object} params
         *
         * @return {Future}
         * @resolve {Dimension}
         * @reject {TypeError|ApiError}
         * @cancel
         */
        updateDimension({commit}, {dimension, language = null, params}) {
            const correctLanguage = isNil(language)
                ? dimension.languageData.currentLanguage
                : language;

            return updateDimension(dimension, correctLanguage, params)
                .chain(result => {
                    commit("patchDimension", {dimension: result});
                    return Future.of(result);
                })
                // TODO: remove this
                // Patches the dimension manually and incredibly stupidly
                // just so that the app seems to work without the api.
                .chainRej(error => {
                    for (const key in params) {
                        if (!isNil(dimension[key])) {
                            dimension[key] = params[key];
                        }
                    }
                    // This commit isn't technically necessary, since the object
                    // is mutated directly above, but it let's us use the
                    // devtools while playing around without api.
                    commit("patchDimension", {dimension});
                    // This prevents us from seeing any errors.
                    return Future.of(dimension);
                });
        },
        /**
         * Add a new ConcreteQuestion to the ConcreteDimension.
         *
         * @param commit
         * @param rootGetters
         * @param {ConcreteDimension} dimension
         * @param {String} text
         * @param {Range} range
         *
         * @return {Future}
         * @resolve {ConcreteQuestion}
         * @reject {TypeError|ApiError}
         * @cancel
         */
        addConcreteQuestion({commit, rootGetters},
                            {
                                dimension,
                                params: {text, range}
                            }) {
            if (dimension.isShadow) {
                return Future.reject(
                    new ValidationError(
                        "AddConcreteQuestion may not be called on ShadowDimension.",
                        {}
                    )
                );
            }

            return addConcreteQuestion(
                dimension,
                rootGetters["session/dataClient"],
                text,
                range
            ).chain(concreteQuestion => {
                commit(
                    "addQuestionToDimension",
                    {
                        dimension,
                        question: concreteQuestion
                    }
                );
                commit(
                    "questions/patchQuestion",
                    {question: concreteQuestion},
                    {root: true}
                );
                return Future.of(concreteQuestion);
            })
        },
        /**
         * Add a new ShadowQuestion to the ConcreteDimension referencing
         * the given ConcreteQuestion.
         *
         * @param commit
         * @param rootGetters
         * @param {ConcreteDimension} dimension
         * @param {ConcreteQuestion} concreteQuestion
         *
         * @return {Future}
         * @resolve {ShadowQuestion}
         * @reject {TypeError|ApiError}
         * @cancel
         */
        addShadowQuestion({commit, dispatch, rootGetters},
                          {
                              dimension,
                              concreteQuestion
                          }) {
            if (dimension.isShadow) {
                return Future.reject(
                    new ValidationError(
                        "AddShadowQuestion may not be called on ShadowDimension.",
                        {}
                    )
                );
            }
            if (concreteQuestion.isShadow) {
                return Future.reject(
                    new ValidationError(
                        "AddShadowQuestion may not be called for ShadowQuestion.",
                        {}
                    )
                );
            }

            return addShadowQuestion(
                dimension,
                rootGetters["session/dataClient"],
                concreteQuestion
            ).chain(shadowQuestion => {
                commit("addQuestionToDimension", {
                    dimension,
                    question: shadowQuestion
                });
                // add the new ShadowQuestion to the Question store
                commit(
                    "questions/patchQuestion",
                    {shadowQuestion},
                    {root: true}
                );
                // Reload the ConcreteQuestion to increase the reference count
                return dispatch(
                    "questions/fetchQuestion",
                    {
                        href: concreteQuestion.href,
                        language: concreteQuestion.languageData.currentLanguage
                    },
                    {root: true}
                    // but still resolve to the ShadowQuestion
                ).map(() => shadowQuestion);
            })
        },
        /**
         * Removes a Question from a ConcreteDimension.
         *
         * @param commit
         * @param {ConcreteDimension} dimension
         * @param {Question} question
         *
         * @return {Future}
         * @resolve {ConcreteDimension}
         * @reject {TypeError|ApiError}
         * @cancel
         */
        removeQuestion({commit}, {dimension, question}) {
            if (dimension.isShadow) {
                return Future.reject(
                    new ValidationError(
                        "RemoveQuestion may not be called on ShadowDimension.",
                        {}
                    )
                );
            }

            return removeQuestion(dimension, question)
                .chain(() => {
                    commit(
                        "removeQuestionFromDimension",
                        {
                            dimension,
                            question
                        }
                    );
                    commit(
                        "questions/removeQuestion",
                        {question},
                        {root: true}
                    );
                    return Future.of(dimension);
                })
        }
    },
    mutations: {
        /**
         * Check, if a Dimension with the given Dimension's id already
         * exists.
         * If so, overwrite the existing one.
         * Otherwise append the new one to the list.
         *
         * @param state
         * @param {Dimension} dimension
         */
        patchDimension(state, {dimension}) {
            let existingDimensionWasReplaced = false;
            state.dimensions = map(
                iDimension => {
                    if (dimension.identifiesWith(iDimension)) {
                        existingDimensionWasReplaced = true;
                        return dimension;
                    }
                    return iDimension;
                },
                state.dimensions
            );
            if (existingDimensionWasReplaced) {
                return;
            }

            state.dimensions.push(dimension);
        },
        /**
         * Removes the given Dimension from the store.
         *
         * Ignored, if the Dimension is not found in the store.
         *
         * @param state
         * @param {Dimension} dimension
         */
        removeDimension(state, {dimension}) {
            state.dimensions = reject(
                bind(dimension.identifiesWith, dimension),
                state.dimensions
            );
        },
        /**
         * Adds a Question to a ConcreteDimension.
         * Overwrites an existing Question, if one with the same id exists.
         *
         * @param state
         * @param {ConcreteDimension} dimension
         * @param {Question} question
         */
        addQuestionToDimension(state, {dimension, question}) {
            if (!isNil(dimension)) {
                let existingQuestionWasReplaced = false;
                dimension.questions = map(
                    iQuestion => {
                        if (question.identifiesWith(iQuestion)) {
                            existingQuestionWasReplaced = true;
                            return question;
                        }
                        return iQuestion;
                    },
                    dimension.questions
                );
                if (existingQuestionWasReplaced) {
                    return;
                }

                dimension.questions.push(question);
            }
        },
        /**
         * Removes a Question from a ConcreteDimension.
         * Does nothing, if the Question isn't found.
         *
         * @param state
         * @param {ConcreteDimension} dimension
         * @param {Question} question
         */
        removeQuestionFromDimension(state, {dimension, question}) {
            if (!isNil(dimension)) {
                dimension.questions = reject(
                    iQuestion => iQuestion.id === question.id,
                    dimension.questions
                );
            }
        }
    }
};

export default store;

export {
    store
};
