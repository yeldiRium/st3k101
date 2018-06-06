import {path, isNil} from "ramda";
import Future from "fluture";

import DataClient from "../../model/DataClient";

import Authentication from "../../api/Authentication";
import Account from "../../api/Model/Account";

/**
 * TODO: refactor API so that DataClient information is returned directly when
 *       logging in.
 */
const store = {
    namespaced: true,
    state: {
        loading: {
            state: "done",
            error: null
        },
        user: null,
        sessionToken: null
    },
    getters: {
        loading: state => {
            return {
                loadingState: state.loading.state,
                error: state.loading.error
            };
        },
        isLoggedIn(state) {
            //return state.sessionToken !== null;
            return true;
        }
    },
    actions: {
        /**
         * Logs in a user with the given credentials, if those match a user.
         * If the API returns an error, this rejects with the reason.
         *
         * @param context
         * @param email
         * @param password
         * @return a Promise.
         * @resolves with the session object.
         * @rejects with a reason for failure.
         */
        logIn(context, email, password) {
            context.commit("setLoadingState", {loadingState: "loading"});
            return Authentication.login(email, password)
                .mapRej(error => {
                    context.commit(
                        "setLoadingState", {
                            loadingState: "error",
                            error: error
                        }
                    );
                    return error;
                })
                .chain(sessionToken => {
                    context.commit("setLoadingState", {loadingState: "done"});
                    context.commit("startSession", {
                        sessionToken
                    });
                })
                .promise()
        },
        /**
         * Ends the current session.
         *
         * @param context
         * @return a Promise.
         * @resolves with True, if the logout process was successful.
         * @rejects with an error message, if not.
         */
        logOut(context) {
            context.commit("setLoadingState", {loadingState: "loading"});
            return Authentication.logout(context.state.sessionToken)
                .chain(data => {
                    context.commit(
                        "setLoadingState", {
                            loadingState: "done"
                        }
                    );
                    context.commit("endSession");
                    return Future.of(true);
                })
                .mapRej(error => {
                    context.commit(
                        "setLoadingState", {
                            loadingState: "error",
                            error: error
                        }
                    );
                    return error;
                })
                .promise();
        },
        /**
         * Retrieves the account data for the currently logged in user.
         * Only works, if a logIn was executed and successful, since it relies
         * on cookies set by the API.
         *
         * @param commit
         * @return a Promise.
         * @resolves with the account object.
         * @rejects with an error message.
         */
        fetchAccount({commit}) {
            if (isNil(state.sessionToken)) {
                return Promise.reject("Not logged in.");
            }

            context.commit("setLoadingState", {loadingState: "loading"});
            return Account.current()
                .chain(data => {
                    let email = path(["fields", "email"], data);
                    let language = path(["fields", "locale_name"], data);

                    context.commit(
                        "setLoadingState", {
                            loadingState: "done"
                        }
                    );
                    // TODO: set correct href
                    commit("setDataClient", new DataClient(
                        "randomHref",
                        email,
                        language
                    ));

                    return Future.of({
                        email,
                        language
                    });
                })
                .mapRej(error => {
                    context.commit(
                        "setLoadingState", {
                            loadingState: "error",
                            error: error
                        }
                    );
                    return error;
                })
                .promise();
        }
    },
    mutations: {
        setLoadingState(state, {loadingState, error}) {
            state.loading.state = loadingState;
            state.loading.error = error;
        },
        startSession(state, {sessionToken}) {
            state.sessionToken = sessionToken;
        },
        endSession(state) {
            state.sessionToken = null;
            state.account = {
                email: null,
                language: null
            };
        },
        setDataClient(state, dataClient) {
            state.account = dataClient;
        }
    }
};

export default store;

export {
    store
};
