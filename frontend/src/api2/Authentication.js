import Future from "fluture";

import {buildApiUrl} from "./Util/Path";
import {checkStatus, extractJson} from "./Util/Response";
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
            mode: "cors",
            data: JSON.stringify({
                email,
                password
            }),
            signal
        })
            .then(resolve)
            .catch(reject);

        return controller.abort;
    })
        .chain(checkStatus)
        .chainRej(extractJson)
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