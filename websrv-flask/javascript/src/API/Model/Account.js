import Future from "fluture";
import ResultHandling from "../Utility/ResultHandling";

export default {
    /**
     * Retrieves the currently logged in user's account data.
     *
     * @returns a Future.
     * @resolves with the current Account's data.
     * @rejects with either a TypeError, if a connection problem occured, or with
     * the server's response detailling the error, if the status code is not
     * 200.
     * @cancel aborts the HTTP request.
     */
    "current": function () {
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;

            fetch("/api/account/current", {
                "credentials": "include",
                signal
            })
                .then(resolve)
                .catch(reject);

            return controller.abort;
        })
            .chain(ResultHandling.checkStatus(200));
    },
    /**
     * Updates the currently logged in account.
     *
     * @param email
     * @param locale
     * @returns a Future.
     * @resolves with the server's response to the update request.
     * @rejects with either a TypeError, if a connection problem occured, or with
     * the server's response detailling the error, if the status code is not
     * 200.
     * @cancel aborts the HTTP request.
     */
    "update": function ({email = null, locale = null}) {
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;
            fetch(
                "/api/account/current",
                {
                    "method": "PUT",
                    "mode": "cors",
                    "credentials": "include",
                    "body": JSON.stringify({
                        email,
                        locale
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
            .chain(ResultHandling.checkStatus(200));
    }
}
