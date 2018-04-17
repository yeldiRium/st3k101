import Future from "fluture";
import ResultHandling from "../Utility/ResultHandling";

export default {
    /**
     * Retrieves the currently logged in user's account data.
     *
     * @returns A Future.
     * @resolve The current Account's data.
     * @reject With data if the response was not ok (=200). With TypeError, if
     * the connection was interrupted somehow.
     * @cancel Aborts the HTTP request.
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
     * @returns A Future.
     * @resolve With the server's response to the update request.
     * @reject With either a TypeError, if a connection problem occured, or with
     * the server's response detailling the error, if the status code is not
     * 200.
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
