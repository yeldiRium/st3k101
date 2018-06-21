import {bind, find, isNil, map, reject} from "ramda";
import Future from "fluture";

import {fetchQuestion, updateQuestion} from "../../api/Question";

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
            return id => {
                find(
                    question => question.id === id,
                    state.questions
                )
            }
        },
        questionByHref(state) {
            return href => {
                find(
                    question => question.href === href,
                    state.questions
                )
            }
        }
    },
    actions: {
        /**
         * Fetches the Question in a certain Language via the API.
         * If the Question is already in the store, it will be
         * overwritten with the API result. Otherwise the Question is
         * added.
         *
         * @param commit
         * @param {String} href
         * @param {Language} language
         *
         * @return {Future}
         * @resolve {Question} to true
         * @reject {TypeError|ApiError}
         * @cancel
         */
        fetchQuestion({commit}, {href, language}) {
            return fetchQuestion(href, language)
                .chain(question => {
                    commit("patchQuestion", {question});
                    return Future.of(question);
                });
        },
        /**
         * Updates the given params on the Question and updates the
         * Question in the store. Translatable fields are set in the given
         * language or the Questions current language.
         *
         * @param commit
         * @param {Question} question
         * @param {Language} language
         * @param {Object} params
         *
         * @return {Future}
         * @resolve {Question}
         * @reject {TypeError|ApiError}
         * @cancel
         */
        updateQuestion({commit}, {question, language = null, params}) {
            const correctLanguage = isNil(language)
                ? question.languageData.currentLanguage
                : language;

            return updateQuestion(question, correctLanguage, params)
                .chain(result => {
                    commit("patchQuestion", {question: result});
                    return Future.of(result);
                })
                // TODO: remove this
                // Patches the question manually and incredibly stupidly
                // just so that the app seems to work without the api.
                .chainRej(error => {
                    for (const key in params) {
                        if (!isNil(question[key])) {
                            question[key] = params[key];
                        }
                    }
                    // This commit isn't technically necessary, since the object
                    // is mutated directly above, but it let's us use the
                    // devtools while playing around without api.
                    commit("patchQuestion", {question});
                    // This prevents us from seeing any errors.
                    return Future.of(question);
                });
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
                        existingQuestionWasReplaced = true;
                        return question;
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
