import Future from "fluture";
import {prop} from "ramda";
import {checkStatus, extractJson, extractJsonAndReject} from "./Util/Response";
import {parseDataClient} from "./Util/Parse";
import {fetchApi} from "./Util/Request";

/**
 * Register a new DataClient.
 *
 * @param {String} email
 * @param {String} password
 * @return {Future}
 * @resolve {DataClient}
 * @reject with API error message
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
        .chain(checkStatus(200))
        .chainRej(extractJsonAndReject)
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
 * @reject with API error message
 * @cancel TODO: is this cancellable?
 */
function requestSession(email, password) {
    return fetchApi("/api/session", {
        method: "POST",
        body: JSON.stringify({
            email,
            password
        })
    })
        .chain(checkStatus(200))
        .chainRej(extractJsonAndReject)
        .chain(extractJson)
        .map(prop("session_token"));
}

/**
 * Ends a Session.
 *
 * @param {String} sessionToken
 * @return {Future}
 * @resolve to true
 * @reject with API error message
 * @cancel TODO: is this cancellable?
 */
function endSession(sessionToken) {
    return Future.reject("Please implement this.");
}

export {
    register,
    requestSession,
    endSession
};