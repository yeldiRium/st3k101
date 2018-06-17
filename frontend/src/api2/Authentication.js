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
 * @reject {Object} with API error message
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
 * @reject {Object} with API error message
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
 * @param {String} sessionToken
 * @return {Future}
 * @resolve {Boolean} to true
 * @reject {Object} with API error object
 * @cancel see fetchApi
 */
function endSession(sessionToken) {
    return fetchApi("/api/session", {
        method: "DELETE",
        authenticate: true
    })
        .map(() => true);
}

export {
    register,
    requestSession,
    endSession
};