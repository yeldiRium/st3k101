import Future from "fluture";
import ResultHandling from "../Utility/ResponseHandling";
import PathHandling from "../Utility/PathHandling";

export default {
    /**
     * Retrieves the currently logged in user's account data.
     *
     * @returns a Future.
     * @resolves with the current Account's data.
     * @rejects with either a TypeError, if a connection problem occured, or
     * with the server's response detailling the error, if the status code is
     * not 200.
     * @cancel aborts the HTTP request.
     */
    "current": function () {
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;

            fetch(PathHandling.buildApiPath("/api/account/current"), {
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
     * Updates the currently logged in account.
     *
     * @param email
     * @param language
     * @returns a Future.
     * @resolves with the server's response to the update request.
     * @rejects with either a TypeError, if a connection problem occured, or
     * with the server's response detailling the error, if the status code is
     * not 200.
     * @cancel aborts the HTTP request.
     */
    "update": function ({email = null, language = null}) {
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;
            fetch(
                "/api/account/current",
                {
                    "method": "PUT",
                    "mode": "cors",
                    "body": JSON.stringify({
                        email,
                        "locale": language
                    }),
                    "headers": {
                        "Content-Type": "application/json"
                    },
                    signal
                }
            )
                .then(resolve)
                .catch(reject);

            return controller.abort;
        })
            .chain(ResultHandling.checkStatus(200))
            .chain(ResultHandling.extractJson)
            .chainRej(ResultHandling.extractJson);
    }
}
