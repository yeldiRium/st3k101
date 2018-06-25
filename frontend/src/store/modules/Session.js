import {isNil, path} from "ramda";
import Future from "fluture";

import {getItem, removeItem, setItem} from "../Utility/cookies";

import DataClient from "../../model/DataClient";
import {
    endSession,
    getCurrentDataClient,
    register,
    requestSession
} from "../../api/Authentication";

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
        /**
         * Registers a new DataClient without setting any state.
         *
         * @param context
         * @param email
         * @param password
         * @returns {Future}
         * @resolve {DataClient}
         * @reject {TypeError|ApiError}
         * @cancel
         */
        register(context, {email, password}) {
            return register(email, password);
        },
        /**
         * Requests a Session from the API and stores it, if the credentials are
         * correct.
         *
         * @param context
         * @param email
         * @param password
         * @returns {Future}
         * @resolve {String} to the session token
         * @reject {TypeError|ApiError}
         * @cancel
         */
        requestSession(context, {email, password}) {
            return requestSession(email, password)
                .chain(sessionToken =>
                    context.dispatch("startSession", {sessionToken})
                        .map(() => sessionToken)
                );
        },
        /**
         * Resumes a session stored in a cookie, if one exists.
         * Otherwise rejects.
         *
         * The dispatch to startSession will reject, if the sessionToken found
         * was invalid.
         *
         * @param context
         * @returns {Future}
         * @resolve {DataClient}
         * @reject {TypeError|ApiError}
         * @cancel
         */
        resumeSessionFromCookie(context) {
            return Future((reject, resolve) => {
                const sessionToken = getItem("sessionToken");
                if (!isNil(sessionToken)) {
                    resolve(sessionToken);
                    return;
                }
                reject("No session cookie found.");
            })
                .chain(sessionToken =>
                    context.dispatch("startSession", {sessionToken}))
                .chainRej(error => {
                    context.commit("endSession");
                    removeItem("sessionToken");
                    return Future.reject(error);
                });
        },
        /**
         * Starts the Session, sets the cookie and retrieves the DataClient.
         *
         * @param context
         * @param sessionToken
         * @returns {Future}
         * @resolve {DataClient}
         * @reject {TypeError|ApiError}
         * @cancel
         */
        startSession(context, {sessionToken}) {
            return Future((reject, resolve) => {
                context.commit("startSession", {sessionToken});
                resolve();
            })
            // Set the session cookie after starting the session
                .chain(() => context.dispatch("updateSessionCookie"))
                // retrieve the now logged in DataClient
                .chain(() => context.dispatch("fetchCurrentDataClient"));
        },
        /**
         * Ends the Session on the server and on the client.
         *
         * @param context
         * @returns {Future}
         * @resolve {Boolean} to true
         * @reject {TypeError|ApiError}
         * @cancel
         */
        endSession(context) {
            return endSession()
                .chain(() => {
                    context.commit("endSession");
                    removeItem("sessionToken");
                    return Future.of(true);
                });
        },
        fetchCurrentDataClient(context) {
            return getCurrentDataClient()
                .chain(dataClient => {
                    context.commit("setDataClient", {dataClient});
                    return Future.of(dataClient);
                });
        },
        /**
         * Set session token cookie.
         *
         * @returns {Future}
         * @resolve {null}
         * @reject {null}
         * @cancel
         */
        updateSessionCookie(context) {
            return Future((reject, resolve) => {
                if (context.getters["isLoggedIn"]) {
                    const sessionToken = context.getters["sessionToken"];
                    // TODO: set cookie to secure mode, once efla supports https
                    const expires = new Date();
                    expires.setDate(expires.getMinutes() + 20);
                    setItem("sessionToken", sessionToken, expires);
                    resolve("Session cookie updated.");
                    return;
                }
                reject("Not logged in; Can't update session cookie.");
            });
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
    return rootStore.dispatch(`${namespace}/resumeSessionFromCookie`)
    // Chain rejection to resolving future, so that the initialization process
    // succeeds either way.
        .chainRej(() => Future.of("No session resumed."));
};

export default store;

export {
    store,
    initialize
};
