import Future from "fluture";
import {curry} from "ramda";

export default {
    "extractDataAndLocale": function (result) {
        return {
            "data": result.data,
            "locale": result.headers("Content-Language")
        };
    },
    "extractData": function (result) {
        return result.data;
    },

    /**
     * Checks if the given HTTP Response has the happyCode status code.
     *
     * Returns the Reponse's json content if so, otherwise throws an ApiError.
     *
     * @param {int} happyCode The status code the client wants to receive.
     * @param {Response} response
     * @return Future
     * @resolve With the Response's JSON content.
     * @reject With the Response's JSON content.
     * @throws ApiError
     */
    "checkStatus": curry(function (happyCode, response) {
        let jsonFuture = Future.tryP(() => response.json());

        if (response.status != happyCode) {
            // Reject with the JSON content.
            jsonFuture = jsonFuture.swap();
        }

        return jsonFuture;
    })
}
