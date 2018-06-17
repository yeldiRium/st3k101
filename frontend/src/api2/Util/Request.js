import {always, assoc, identity, ifElse, isNil} from "ramda";
import Future from "fluture";

import {buildApiUrl} from "./Path";

import store from "../../store";

class AuthenticationError extends Error {
    constructor(s) {
        super(s);
    }
}

/**
 * Read the current sessionToken from the vuex store and build authentication
 * headers from it.
 *
 * @param {Boolean} authenticate
 * @returns {Object}
 */
function getAuthenticationHeaders(authenticate = true) {
    const sessionToken = store.getters["session/sessionToken"];

    if (authenticate) {
        return {
            Authentication: `Bearer ${sessionToken}`
        };
    } else {
        return {};
    }
}

function refreshSessionCookieOnSuccessfulRequest(response) {
    if (response.status === 200) {
        return Future.tryP(() => store.dispatch("session/updateSessionCookie"))
            .map(() => response);
    }
    return Future.of(response);
}

const defaultHeaders = {
    "Content-Type": "application/json"
};

/**
 * Fetches a resource with added behaviour.
 *
 * This is tightly coupled to the used vuex store, since it reads the currently
 * logged in DataClient's sessionToken for authentication purposes.
 * It also updates the SessionTokenCookie, if an authenticated request was
 * successful.
 *
 * @param {String} path
 * @param {String} method
 * @param {String} body
 * @param {Object<String>} headers
 * @param {Boolean} authenticate
 *
 * @return {Future}
 * @resolve {Response}
 * @reject {TypeError|AuthenticationError} TypeError on network error,
 *      AuthenticationError on - who would have guessed - authentication error.
 * @cancel cancels the http request
 */
function fetchApi(path,
                  {
                      method = "GET",
                      body = "",
                      headers = {},
                      authenticate = false
                  }) {
    if (authenticate && !store.getters["session/isLoggedIn"]) {
        return Future.reject(
            new AuthenticationError("Authentication failed.")
        );
    }

    let result = Future((reject, resolve) => {
        const controller = new AbortController();
        const signal = controller.signal;

        const useHeaders = {
            ...defaultHeaders,
            ...headers,
            ...getAuthenticationHeaders(authenticate)
        };

        fetch(buildApiUrl(path), {
            method,
            body,
            headers: useHeaders,
            signal
        })
            .then(resolve)
            .catch(reject);

        return controller.abort;
    });

    if (authenticate) {
        return result.chain(refreshSessionCookieOnSuccessfulRequest);
    } else {
        return result;
    }
}

export {
    fetchApi
};