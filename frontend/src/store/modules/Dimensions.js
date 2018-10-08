import {
  allPass,
  bind,
  clone,
  filter,
  find,
  isNil,
  map,
  pipe,
  prop,
  reject,
  uniq,
  without
} from "ramda";
import * as Future from "fluture/index.js";

import {
  addConcreteQuestion,
  addShadowQuestion,
  fetchDimension,
  fetchDimensionById,
  fetchDimensionTemplates,
  removeQuestion,
  updateDimension
} from "../../api/Dimension";
import { BadRequestError, ValidationError } from "../../api/Errors";
import * as R from "ramda";

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
    dimensionById(state, getters, rootState, rootGetters) {
      return function(id) {
        const dimension = clone(
          find(dimension => dimension.id === id, state.dimensions)
        );

        if (isNil(dimension)) {
          return null;
        }

        dimension.questions = map(
          rootGetters["questions/questionById"],
          dimension.questions
        );
        return dimension;
      };
    },
    dimensionByHref(state, getters, rootState, rootGetters) {
      return function(href) {
        const dimension = clone(
          find(dimension => dimension.href === href, state.dimensions)
        );

        if (isNil(dimension)) {
          return null;
        }

        dimension.questions = map(
          rootGetters["questions/questionByid"],
          dimension.questions
        );
        return dimension;
      };
    },
    /**
     * Returns al Dimensions that can be used as templates.
     *
     * @param state
     * @param getters
     * @param rootState
     * @param rootGetters
     * @returns {Array<ConcreteDimension>}
     */
    dimensionTemplates(state, getters, rootState, rootGetters) {
      const dimensions = pipe(
        filter(dimension => dimension.isReadonlyTemplate),
        map(clone)
      )(state.dimensions);
      for (const dimension of dimensions) {
        dimension.dimensions = map(
          rootGetters["questions/questionById"],
          dimension.questions
        );
      }
      return dimensions;
    }
  },
  actions: {
    /**
     * Check, if a Dimension with the given Dimension's id already
     * exists.
     * If so, overwrite the existing one.
     * Otherwise append the new one to the list.
     *
     * Also adds/overwrites all child Questions.
     *
     * Does so bottom up, so that hierarchies are never partially in the
     * store.
     *
     * @param dispatch
     * @param getters
     * @param commit
     * @param {Dimension} dimension
     * @return {Future}
     * @resolve {Dimension}
     * @reject
     * @cancel
     */
    patchDimensionInStore({ dispatch, getters, commit }, { dimension }) {
      const patchQuestionFutures = [];
      for (const question of dimension.questions) {
        patchQuestionFutures.push(
          dispatch(
            "questions/patchQuestionInStore",
            { question },
            { root: true }
          )
        );
      }
      return Future.parallel(Infinity, patchQuestionFutures).chain(() => {
        const oldDimension = getters.dimensionById(dimension.id);
        if (!isNil(oldDimension)) {
          commit("replaceDimension", { dimension });
          if (
            dimension.isConcrete &&
            dimension.template &&
            !dimension.contentEquals(oldDimension)
          ) {
            // update any references to this template in the store, but only if modified
            const futures = R.map(
              reference => dispatch("fetchDimension", reference),
              dimension.ownedIncomingReferences
            );
            return Future.parallel(Infinity, futures).chain(() =>
              Future.of(dimension)
            );
          }
        } else {
          commit("addDimension", { dimension });
        }
        return Future.of(dimension);
      });
    },
    /**
     * Removes the given Dimension from the store.
     *
     * Ignored, if the Dimension is not found in the store.
     *
     * Also removes all child Questions from the store.
     *
     * @param commit
     * @param dispatch
     * @param {Dimension} dimension
     * @returns {Future}
     * @resolve {Boolean} to true
     * @reject
     * @cancel
     */
    removeDimensionFromStore({ commit, dispatch }, { dimension }) {
      return Future((reject, resolve) => {
        commit("removeDimension", { dimension });
        resolve(true);
      }).chain(() => {
        const removeQuestionFutures = [];
        for (const question of dimension.questions) {
          removeQuestionFutures.push(
            dispatch(
              "questions/removeQuestionFromStore",
              { question },
              { root: true }
            )
          );
        }
        return Future.parallel(Infinity, removeQuestionFutures).map(() => true);
      });
    },
    /**
     * Fetches the Dimension in a certain Language via the API.
     * If the Dimension is already in the store, it will be
     * overwritten with the API result. Otherwise the Dimension is
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
     * @resolve {Dimension} to true
     * @reject {TypeError|ApiError}
     * @cancel
     */
    fetchDimension(
      { dispatch, rootGetters },
      { href = null, id = null, language = null }
    ) {
      const authenticationToken = rootGetters["session/sessionToken"];
      let future;
      if (isNil(href) && isNil(id)) {
        return Future.reject(
          new BadRequestError("At least href or id has to be provided.")
        );
      }
      if (!isNil(href)) {
        future = fetchDimension(authenticationToken, href, language);
      } else {
        future = fetchDimensionById(authenticationToken, id, language);
      }
      return future.chain(dimension =>
        dispatch("patchDimensionInStore", { dimension })
      );
    },
    /**
     * Fetches a list of all available template Dimensions.
     *
     * @param dispatch
     * @param rootGetters
     * @param {Language} language on optional language in which the list should be
     *  retrieved
     * @returns {Future}
     * @resolve {Array<ConcreteDimension>}
     * @reject {TypeError|ApiError}
     * @cancel
     */
    fetchDimensionTemplates({ dispatch, rootGetters }, { language = null }) {
      return fetchDimensionTemplates(
        rootGetters["session/sessionToken"],
        language
      ).chain(templates => {
        const patchTemplateFutures = [];
        for (const template of templates) {
          patchTemplateFutures.push(
            dispatch("patchDimensionInStore", { dimension: template })
          );
        }
        return Future.parallel(Infinity, patchTemplateFutures);
      });
    },
    /**
     * Updates the given params on the Dimension and updates the
     * Dimension in the store. Translatable fields are set in the given
     * language or the Dimensions current language.
     *
     * @param dispatch
     * @param rootGetters
     * @param {Dimension} dimension
     * @param {Language} language
     * @param {Object} params
     *
     * @return {Future}
     * @resolve {Dimension}
     * @reject {TypeError|ApiError}
     * @cancel
     */
    updateDimension(
      { dispatch, rootGetters },
      { dimension, language = null, params }
    ) {
      const correctLanguage = isNil(language)
        ? dimension.languageData.currentLanguage
        : language;

      return updateDimension(
        rootGetters["session/sessionToken"],
        dimension,
        correctLanguage,
        params
      ).chain(result =>
        dispatch("patchDimensionInStore", { dimension: result })
      );
    },
    /**
     * Add a new ConcreteQuestion to the ConcreteDimension.
     *
     * @param commit
     * @param dispatch
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
    addConcreteQuestion(
      { commit, dispatch, rootGetters },
      {
        dimension,
        params: { text, range }
      }
    ) {
      if (dimension.isShadow) {
        return Future.reject(
          new ValidationError(
            "AddConcreteQuestion may not be called on ShadowDimension.",
            {}
          )
        );
      }

      return addConcreteQuestion(
        rootGetters["session/sessionToken"],
        dimension,
        text,
        range
      ).chain(concreteQuestion => {
        commit("addQuestionToDimension", {
          dimension,
          question: concreteQuestion
        });
        return dispatch(
          "questions/patchQuestionInStore",
          { question: concreteQuestion },
          { root: true }
        );
      });
    },
    /**
     * Add a new ShadowQuestion to the ConcreteDimension referencing
     * the given ConcreteQuestion.
     *
     * @param commit
     * @param dispatch
     * @param rootGetters
     * @param {ConcreteDimension} dimension
     * @param {ConcreteQuestion} concreteQuestion
     *
     * @return {Future}
     * @resolve {ShadowQuestion}
     * @reject {TypeError|ApiError}
     * @cancel
     */
    addShadowQuestion(
      { commit, dispatch, rootGetters },
      { dimension, concreteQuestion }
    ) {
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
        rootGetters["session/sessionToken"],
        dimension,
        concreteQuestion
      ).chain(shadowQuestion => {
        commit("addQuestionToDimension", {
          dimension,
          question: shadowQuestion
        });
        return (
          dispatch(
            "questions/patchQuestionInStore",
            { question: shadowQuestion },
            { root: true }
          )
            // Reload the ConcreteQuestion to increase the reference count
            .chain(() =>
              dispatch(
                "questions/fetchQuestion",
                {
                  href: concreteQuestion.href,
                  language: concreteQuestion.languageData.currentLanguage
                },
                { root: true }
              )
            )
            // but still resolve to the ShadowQuestion
            .map(() => shadowQuestion)
        );
      });
    },
    /**
     * Removes a Question from a ConcreteDimension.
     *
     * @param commit
     * @param dispatch
     * @param rootGetters
     * @param {ConcreteDimension} dimension
     * @param {Question} question
     *
     * @return {Future}
     * @resolve {ConcreteDimension}
     * @reject {TypeError|ApiError}
     * @cancel
     */
    removeQuestion({ commit, dispatch, rootGetters }, { dimension, question }) {
      if (dimension.isShadow) {
        return Future.reject(
          new ValidationError(
            "RemoveQuestion may not be called on ShadowDimension.",
            {}
          )
        );
      }

      return removeQuestion(
        rootGetters["session/sessionToken"],
        dimension,
        question
      ).chain(() => {
        commit("removeQuestionFromDimension", {
          dimension,
          question
        });
        return dispatch(
          "questions/removeQuestionFromStore",
          { question },
          { root: true }
        );
      });
    }
  },
  mutations: {
    /**
     * Adds a dimension to the store.
     *
     * @param state
     * @param {Dimension} dimension
     */
    addDimension(state, { dimension }) {
      const sparseDimension = dimension.clone();
      sparseDimension.questions = map(prop("id"), sparseDimension.questions);
      state.dimensions.push(sparseDimension);
    },
    /**
     * Replaces a dimension in the store.
     * Does not replace a writeable dimension by a readonly template.
     *
     * @param state
     * @param {Dimension} dimension
     */
    replaceDimension(state, { dimension }) {
      const sparseDimension = dimension.clone();
      sparseDimension.questions = map(prop("id"), sparseDimension.questions);
      state.dimensions = reject(
        allPass([
          iDimension => iDimension.identifiesWith(sparseDimension),
          // do not replace a fully accessible dimension by a readonly template
          iDimension =>
            iDimension.isReadonlyTemplate || !sparseDimension.isReadonlyTemplate
        ]),
        state.dimensions
      );
      state.dimensions.push(sparseDimension);
    },
    /**
     * Removes the given Dimension from the store.
     *
     * Ignored, if the Dimension is not found in the store.
     *
     * @param state
     * @param {Dimension} dimension
     */
    removeDimension(state, { dimension }) {
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
    addQuestionToDimension(state, { dimension, question }) {
      const dimensionInStore = find(
        bind(dimension.identifiesWith, dimension),
        state.dimensions
      );

      if (!isNil(dimensionInStore)) {
        dimensionInStore.questions.push(question.id);
        dimensionInStore.questions = uniq(dimensionInStore.questions);
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
    removeQuestionFromDimension(state, { dimension, question }) {
      const dimensionInStore = find(
        bind(dimension.identifiesWith, dimension),
        state.dimensions
      );

      if (!isNil(dimensionInStore)) {
        dimensionInStore.questions = without(
          [question.id],
          dimensionInStore.questions
        );
      }
    }
  }
};

export default store;

export { store };
