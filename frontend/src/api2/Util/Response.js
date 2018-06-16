import {curry} from "ramda";
import Future from "fluture";

/**
 * Checks if the given HTTP Response has the happyCode status code.
 * Resolves with the Response, if the status code matched, rejects with it
 * otherwise.
 *
 * @param {int} happyCode The status code the client wants to receive.
 * @param {Response} response
 * @return Future
 * @resolves with the Response.
 * @rejects with the Response.
 */
const checkStatus = curry(function (happyCode, response) {
    if (response.status != happyCode) {
        // Reject with the JSON content.
        return Future.reject(response);
    }

    return Future.of(response);
});

/**
 * Extracts the JSON content from a response.
 *
 * @param {Response} response
 * @returns a Future.
 * @resolves with the Response's JSON content.
 * @reject see response.json()
 */
const extractJson = function (response) {
    console.log(response);
    return Future.tryP(() => response.json());
};

/**
 * Extracts the JSON content from a response and forces the Future to reject.
 *
 * @param {Response} response
 * @returns a Future.
 * @resolves never
 * @reject with the Response's JSON content
 */
const extractJsonAndReject = function (response) {
    console.log(response);
    return Future.tryP(() => response.json())
        .chain(Future.reject);
};

/**
 * Extracts the JSON content and the content-language from a response.
 *
 * @param {Response} response
 * @returns {Future}.
 * @resolves with the Response's JSON content and content-language.
 * @rejects see response.json()
 */
const extractJsonPlusLanguage = function (response) {
    return Future.tryP(() => response.json())
        .map(data => ({
            "data": data,
            "language": response.headers.get("Content-Language")
        }));
};

export {
    checkStatus,
    extractJson,
    extractJsonAndReject,
    extractJsonPlusLanguage
};