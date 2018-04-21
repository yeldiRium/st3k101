import Future from "fluture";
import {curry} from "ramda";

export default {
    "extractDataAndLanguage": function (result) {
        return {
            "data": result.data,
            "language": result.headers("Content-Language")
        };
    },
    "extractData": function (result) {
        return result.data;
    },

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
    "checkStatus": curry(function (happyCode, response) {
        if (response.status != happyCode) {
            // Reject with the JSON content.
            return Future.reject(response);
        }

        return Future.of(response);
    }),

    /**
     * Extracts the JSON content from a response.
     *
     * @param {Response} response
     * @returns a Future.
     * @resolves with the Response's JSON content.
     */
    "extractJson": function (response) {
        console.log(response);
        return Future.tryP(() => response.json());
    },

    /**
     * Extracts the JSON content and the content-language from a response.
     *
     * @param {Response} response
     * @returns a Future.
     * @resolves with the Response's JSON content and content-language.
     */
    "extractJsonPlusLanguage": function (response) {
        return Future.tryP(() => response.json())
            .map(data => ({
                "data": data,
                "language": response.headers.get("Content-Language")
            }));
    }
}
