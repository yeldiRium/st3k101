import {always, assoc, identity, ifElse, isNil} from "ramda";
import Future from "fluture";

import {buildApiUrl} from "./Path";
import {categorizeResponse} from "./Response";
import {AuthenticationError} from "../Errors";

import store from "../../store";

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
            Authorization: `Bearer ${sessionToken}`
        };
    } else {
        return {};
    }
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
 * Also pre-parses the result and categorizes errors.
 *
 * @param {String} path
 * @param {String} method
 * @param {String} body
 * @param {Object<String>} headers
 * @param {Boolean} authenticate
 *
 * @return {Future}
 * @resolve {Response}
 * @reject {TypeError|ApiError} TypeError on network error, for the rest see
 *      categorizeResponse.
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
            new AuthenticationError("User not logged in.")
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

        const fetchParams = {
            method,
            headers: useHeaders,
            signal
        };

        if (method !== "GET" && method !== "HEAD") {
            fetchParams["body"] = body;
        }

        fetch(buildApiUrl(path), fetchParams)
            .then(resolve)
            .catch(reject);

        return controller.abort;
    })
        .chain(categorizeResponse);

    if (authenticate) {
        return result.chain(
            response => store.dispatch("session/updateSessionCookie")
                .map(() => response)
        );
    } else {
        return result;
    }
}

export {
    fetchApi
};
