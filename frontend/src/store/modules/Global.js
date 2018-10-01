const store = {
  namespaced: true,
  state: {
    window: {
      height: 0,
      width: 0
    }
  },
  getters: {},
  actions: {
    fetchAll({ dispatch }) {
      return dispatch("fetchWindowSize");
    },
    registerEventHandlers({ dispatch }) {
      function fetchWindowSize() {
        dispatch("fetchWindowSize");
      }

      window.addEventListener("resize", fetchWindowSize);
    },
    fetchWindowSize({ commit }) {
      commit("setWindowWidth", document.documentElement.clientWidth);
      commit("setWindowHeight", document.documentElement.clientHeight);
    }
  },
  mutations: {
    setWindowWidth(state, width) {
      state.window.width = width;
    },
    setWindowHeight(state, height) {
      state.window.height = height;
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
const initialize = function(rootStore, namespace) {
  return rootStore
    .dispatch(`${namespace}/fetchAll`)
    .chain(() => rootStore.dispatch(`${namespace}/registerEventHandlers`));
};

export { store, initialize };
