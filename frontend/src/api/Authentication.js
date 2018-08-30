import Future from "fluture";
import {prop} from "ramda";
import {checkStatus, extractJson} from "./Util/Response";
import {parseDataClient} from "./Util/Parse";
import {fetchApi} from "./Util/Request";

/**
 * Register a new DataClient.
 *
 * @param {String} email
 * @param {String} password
 * @return {Future}
 * @resolve {DataClient}
 * @reject {TypeError|ApiError}
 * @cancel see fetchApi
 */
function register(email, password) {
    return fetchApi("/api/dataclient", {
        method: "POST",
        body: JSON.stringify({
            email,
            password
        })
    })
        .chain(extractJson)
        .map(parseDataClient);
}

/**
 * Requests a Session Token for a DataClient.
 *
 * @param {String} email
 * @param {String} password
 * @return {Future}
 * @resolve {String} to session token.
 * @reject {TypeError|ApiError}
 * @cancel see fetchApi
 */
function requestSession(email, password) {
    return fetchApi("/api/session", {
        method: "POST",
        body: JSON.stringify({
            email,
            password
        })
    })
        .chain(extractJson)
        .map(prop("session_token"));
}

/**
 * Ends a Session.
 *
 * @param {String} authenticationToken
 * @return {Future}
 * @resolve {Boolean} to true
 * @reject {TypeError|ApiError}
 * @cancel see fetchApi
 */
function endSession(authenticationToken) {
    return fetchApi("/api/session", {
        method: "DELETE",
        authenticationToken
    })
        .map(() => true);
}

/**
 * Retrieves the currently logged in DataClient.
 * Obviously only works when authenticated.
 *
 * @param {String} authenticationToken
 * @return {Future}
 * @resolve {DataClient}
 * @reject {TypeError|ApiError}
 * @cancel see fetchApi
 */
function getCurrentDataClient(authenticationToken) {
    return fetchApi("/api/dataclient", {
        authenticationToken
    })
        .chain(extractJson)
        .map(parseDataClient);
}

export {
    register,
    requestSession,
    endSession,
    getCurrentDataClient
};
