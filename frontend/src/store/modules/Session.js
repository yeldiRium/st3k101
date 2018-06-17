import {isNil, path} from "ramda";

import DataClient from "../../model/DataClient";

const store = {
    namespaced: true,
    state: {
        /** @type {DataClient} */
        dataClient: null,
        sessionToken: null
    },
    getters: {
        isLoggedIn(state) {
            return state.sessionToken !== null;
        },
        sessionToken(state) {
            return state.sessionToken;
        },
        dataClient(state) {
            return state.dataClient;
        }
    },
    actions: {
        startSession(context, {sessionToken, dataClient}) {
            context.commit("startSession", {sessionToken});
            // TODO: fetch DataClient here
        },
        endSession(context) {
            context.commit("endSession");
        }
    },
    mutations: {
        startSession(state, {sessionToken}) {
            state.sessionToken = sessionToken;
        },
        endSession(state) {
            state.sessionToken = null;
            state.dataClient = null;
        },
        setDataClient(state, {dataClient}) {
            state.dataClient = dataClient;
        }
    }
};

export default store;

export {
    store
};
