import Future from "fluture";

import ResultHandling from "../Utility/ResultHandling";
import PathHandling from "../Utility/PathHandling";

export default {
    /**
     * Lists all Surveys available to the current user.
     *
     * @returns a Future.
     * @resolves with the server's confirmation response.
     * @rejects with either a TypeError, if a connection problem occured, or
     * with the server's response detailling the error, if the status code is
     * not 200.
     * @cancel aborts the HTTP request.
     */
    "all": function () {
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;
            fetch(PathHandling.buildApiPath("/api/survey"), {
                "method": "GET",
                "mode": "cors",
                "credentials": "include",
                signal
            })
                .then(resolve)
                .catch(reject);

            return controller.abort;
        })
            .chain(ResultHandling.checkStatus(200))
            .chain(ResultHandling.extractJsonPlusLanguage)
            .chainRej(ResultHandling.extractJson);
    },
    /**
     * Creates a new survey with the given name.
     * It's original language will be the currently active one.
     *
     * @param name
     * @returns a Future.
     * @resolves with the server's confirmation response.
     * @rejects with either a TypeError, if a connection problem occured, or
     * with the server's response detailling the error, if the status code is
     * not 200.
     * @cancel aborts the HTTP request.
     */
    "create": function (name) {
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;
            fetch(PathHandling.buildApiPath("/api/survey"), {
                "method": "POST",
                "headers": {
                    "Content-Type": "application/json"
                },
                "mode": "cors",
                "credentials": "include",
                "body": JSON.stringify({
                    "name": name
                }),
                signal
            })
                .then(resolve)
                .catch(reject);

            return controller.abort;
        })
            .chain(ResultHandling.checkStatus(200))
            .chain(ResultHandling.extractJson)
            .chainRej(ResultHandling.extractJson);
    },
    /**
     * Update the Survey with the given uuid.
     *
     * @param uuid
     * @param name
     * @returns a Future.
     * @resolves with the server's confirmation response.
     * @rejects with either a TypeError, if a connection problem occured, or
     * with the server's response detailling the error, if the status code is
     * not 200.
     * @cancel aborts the HTTP request.
     */
    "update": function (uuid, name) {
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;
            fetch(PathHandling.buildApiPath(`/api/survey/${uuid}`), {
                "method": "PUT",
                "headers": {
                    "Content-Type": "application/json"
                },
                "mode": "cors",
                "credentials": "include",
                "body": JSON.stringify({
                    "name": name
                }),
                signal
            })
                .then(resolve)
                .catch(reject);

            return controller.abort;
        })
            .chain(ResultHandling.checkStatus(200))
            .chain(ResultHandling.extractJson)
            .chainRej(ResultHandling.extractJson);
    },
    /**
     * Deletes the Survey with the given uuid.
     *
     * @param uuid
     * @returns a Future.
     * @resolves with the server's confirmation response.
     * @rejects with either a TypeError, if a connection problem occured, or
     * with the server's response detailling the error, if the status code is
     * not 200.
     * @cancel aborts the HTTP request.
     */
    "delete": function (uuid) {
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;
            fetch(PathHandling.buildApiPath(`/api/survey/${uuid}`), {
                "method": "DELETE",
                "mode": "cors",
                "credentials": "include",
                signal
            })
                .then(resolve)
                .catch(reject);

            return controller.abort;
        })
            .chain(ResultHandling.checkStatus(200))
            .chain(ResultHandling.extractJson)
            .chainRej(ResultHandling.extractJson);
    }
}
