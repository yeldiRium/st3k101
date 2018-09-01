import {bind, filter, find, isNil, map, pipe, reject} from "ramda";
import Future from "fluture";

import {
    fetchQuestion,
    fetchQuestionById,
    fetchQuestionTemplates,
    updateQuestion
} from "../../api/Question";
import {BadRequestError} from "../../api/Errors";

const store = {
    namespaced: true,
    state: {
        /**
         * All Questions that have been loaded from the API.
         *
         * @type {Array<Question>}
         */
        questions: []
    },
    getters: {
        questionById(state) {
            return id => find(
                question => question.id === id,
                state.questions
            )
        },
        questionByHref(state) {
            return href => find(
                question => question.href === href,
                state.questions
            )
        },
        /**
         * Returns al Questions that can be used as templates.
         *
         * @param state
         * @param getters
         * @param rootState
         * @param rootGetters
         * @returns {Array<ConcreteQuestion>}
         */
        questionTemplates(state, getters, rootState, rootGetters) {
            return filter(
                question => question.template,
                state.questions
            );
        }
    },
    actions: {
        /**
         * Check, if a Question with the given Question's id already
         * exists.
         * If so, overwrite the existing one.
         * Otherwise append the new one to the list.
         *
         * @param commit
         * @param {Question} question
         * @return {Future}
         * @resolve {Question}
         * @reject
         * @cancel
         */
        patchQuestionInStore({commit}, {question}) {
            return Future((reject, resolve) => {
                commit("patchQuestion", {question});
                resolve(question);
            });
        },
        /**
         * Removes the given Question from the store.
         *
         * Ignored, if the Question is not found in the store.
         *
         * @param commit
         * @param {Question} question
         * @returns {Future}
         * @resolve {Boolean} to true
         * @reject
         * @cancel
         */
        removeQuestionFromStore({commit}, {question}) {
            return Future((reject, resolve) => {
                commit("removeQuestion", {question});
                resolve(true);
            });
        },
        /**
         * Fetches the Question in a certain Language via the API.
         * If the Question is already in the store, it will be
         * overwritten with the API result. Otherwise the Question is
         * added.
         *
         * At least one of href and id must be provided.
         *
         * @param dispatch
         * @param rootGetters
         * @param {String} href
         * @param id
         * @param {Language} language
         *
         * @return {Future}
         * @resolve {Question} to true
         * @reject {TypeError|ApiError}
         * @cancel
         */
        fetchQuestion({dispatch, rootGetters}, {href = null, id = null, language = null}) {
            const authenticationToken = rootGetters["session/sessionToken"];
            let future;
            if (isNil(href) && isNil(id)) {
                return Future.reject(
                    new BadRequestError("At least href or id has to be provided.")
                );
            }
            if (!isNil(href)) {
                future = fetchQuestion(authenticationToken, href, language);
            } else {
                future = fetchQuestionById(
                    authenticationToken,
                    id,
                    language
                );
            }
            return future
                .chain(question => dispatch(
                    "patchQuestionInStore",
                    {question}
                ));
        },
        /**
         * Fetches a list of all available template Questions.
         *
         * @param dispatch
         * @param rootGetters
         * @param {Language} language on optional language in which the list should be
         *  retrieved
         * @returns {Future}
         * @resolve {Array<ConcreteQuestion>}
         * @reject {TypeError|ApiError}
         * @cancel
         */
        fetchQuestionTemplates({dispatch, rootGetters}, {language = null}) {
            return fetchQuestionTemplates(
                rootGetters["session/sessionToken"],
                language
            )
                .chain(templates => {
                    const patchTemplateFutures = [];
                    for (const template of templates) {
                        patchTemplateFutures.push(dispatch(
                            "patchQuestionInStore",
                            {question: template}
                        ));
                    }
                    return Future.parallel(Infinity, patchTemplateFutures);
                });
        },
        /**
         * Updates the given params on the Question and updates the
         * Question in the store. Translatable fields are set in the given
         * language or the Questions current language.
         *
         * @param dispatch
         * @param rootGetters
         * @param {Question} question
         * @param {Language} language
         * @param {Object} params
         *
         * @return {Future}
         * @resolve {Question}
         * @reject {TypeError|ApiError}
         * @cancel
         */
        updateQuestion({dispatch, rootGetters}, {question, language = null, params}) {
            const correctLanguage = isNil(language)
                ? question.languageData.currentLanguage
                : language;

            return updateQuestion(
                rootGetters["session/sessionToken"],
                question,
                correctLanguage,
                params
            )
                .chain(result =>
                    dispatch("patchQuestionInStore", {question: result})
                );
        }
    },
    mutations: {
        /**
         * Check, if a Question with the given Question's id already
         * exists.
         * If so, overwrite the existing one.
         * Otherwise append the new one to the list.
         *
         * @param state
         * @param {Question} question
         */
        patchQuestion(state, {question}) {
            let existingQuestionWasReplaced = false;
            state.questions = map(
                iQuestion => {
                    if (question.identifiesWith(iQuestion)) {
                        if (!question.isReadonlyTemplate || iQuestion.isReadonlyTemplate) {
                            existingQuestionWasReplaced = true;
                            return question;
                        }
                    }
                    return iQuestion;
                },
                state.questions
            );
            if (existingQuestionWasReplaced) {
                return;
            }

            state.questions.push(question);
        },
        /**
         * Removes the given Question from the store.
         *
         * Ignored, if the Question is not found in the store.
         *
         * @param state
         * @param {Question} question
         */
        removeQuestion(state, {question}) {
            state.questions = reject(
                bind(question.identifiesWith, question),
                state.questions
            );
        },
    }
};

export default store;

export {
    store
};
