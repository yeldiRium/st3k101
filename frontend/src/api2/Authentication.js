import Future from "fluture";
import {__} from "ramda";

import {buildApiUrl} from "./Util/Path";
import {checkStatus, extractJson, extractJsonAndReject} from "./Util/Response";
import {parseDataClient} from "./Util/Parse";

/**
 * Register a new DataClient.
 *
 * @param {String} email
 * @param {String} password
 * @return {Future}
 * @resolve {DataClient}
 * @reject with API error message
 * @cancel TODO: is this cancellable?
 */
function register(email, password) {
    return Future((reject, resolve) => {
        const controller = new AbortController();
        const signal = controller.signal;
        fetch(buildApiUrl("/api/dataclient"), {
            method: "POST",
            body: JSON.stringify({
                email,
                password
            }),
            headers: {
                "Content-Type": "application/json"
            },
            signal
        })
            .then(resolve)
            .catch(reject);

        return controller.abort;
    })
        .chain(checkStatus(200))
        .chainRej(extractJsonAndReject)
        .chain(extractJson)
        .map(parseDataClient);
}

/**
 * Requests a Session Token for a DataClient. *
 *
 * @param {String} email
 * @param {String} password
 * @return {Future}
 * @resolve to true
 * @reject with API error message
 * @cancel TODO: is this cancellable?
 */
function requestSession(email, password) {
    return Future.reject("Please implement this.");
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