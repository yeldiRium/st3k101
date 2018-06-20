import {isNil, path} from "ramda";
import Future from "fluture";

import {setItem, getItem} from "../Utility/cookies";

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
        getSessionFromCookie(context) {
            const sessionToken = getItem("session-token");
            if (!isNil(sessionToken)) {
                context.dispatch("startSession", {sessionToken});
            }
        },
        startSession(context, {sessionToken, dataClient}) {
            context.commit("startSession", {sessionToken});

            context.dispatch("updateSessionCookie");

            // TODO: fetch DataClient here
        },
        endSession(context) {
            context.commit("endSession");
        },
        /**
         * Set session token cookie.
         */
        updateSessionCookie(context) {
            if (context.getters["isLoggedIn"]) {
                const sessionToken = context.getters["sessionToken"];
                // TODO: set cookie to secure mode, once efla supports https
                const expires = new Date();
                expires.setDate(expires.getMinutes() + 20);
                setItem("session-token", sessionToken, expires);
            }
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

/**
 * Initializes this store's content.
 *
 * Since actions encase their return value in a resolved Promise (if the value
 * isn't a Promise itself), the Promise's resolving value has to be untangled.
 *
 * Loads a SessionToken from cookie - it one exists.
 * If so, checks, if it is still valid.
 * If so, fetches the according DataClient.
 *
 * @param rootStore The instantiated store.
 * @param namespace The namespace in which this store resides.
 * @return a Future
 * @resolves with nothing.
 * @rejects with nothing.
 * @cancel doesn't exist.
 */
const initialize = function (rootStore, namespace) {
    return rootStore.dispatch(`${namespace}/getSessionFromCookie`);
};

export default store;

export {
    store,
    initialize
};
