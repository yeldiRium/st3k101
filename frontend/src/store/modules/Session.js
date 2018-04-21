import {path} from "ramda";
import Future from "fluture";

import Authentication from "../../api/Authentication";
import Account from "../../api/Model/Account";

const store = {
    namespaced: true,
    state: {
        account: {
            email: null,
            language: null
        },
        sessionToken: null
    },
    actions: {
        /**
         * Logs in a user with the given credentials, if those match a user.
         * If the API returns an error, this rejects with the reason.
         *
         * @param context
         * @param email
         * @param password
         * @return a Future.
         * @resolves with the session object.
         * @rejects with a reason for failure.
         * @cancel
         */
        logIn(context, email, password) {
            return Authentication.login(email, password)
                .chain(sessionToken => {
                    context.commit("startSession", {
                        sessionToken
                    });

                    return Future.tryP(() => context.dispatch("fetchAccount"))
                        .map(account => ({
                            sessionToken,
                            account
                        }));
                });
        },
        /**
         * Ends the current session.
         *
         * @param context
         * @return a Future.
         * @resolves with True, if the logout process was successful.
         * @rejects with an error message, if not.
         * @cancel
         */
        logOut(context) {
            return Authentication.logout(context.state.sessionToken)
                .chain(data => {
                    context.commit("endSession");
                    return Future.of(true);
                });
        },
        /**
         * Retrieves the account data for the currently logged in user.
         * Only works, if a logIn was executed, since it relies on cookies set
         * by the API.
         *
         * @param commit
         * @return a Future.
         * @resolves with the account object.
         * @rejects with an error message.
         * @cancel
         */
        fetchAccount({commit}) {
            return Account.current()
                .chain(data => {
                    let email = path(["fields", "email"], data);
                    let language = path(["fields", "locale_name"], data);

                    commit("setAccountData", {
                        email,
                        language
                    });

                    return Future.of({
                        email,
                        language
                    });
                });
        }
    },
    mutations: {
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
        setAccountData(state, {email, language}) {
            state.account = {
                email,
                language
            };
        }
    }
};

export default store;

export {
    store
};
