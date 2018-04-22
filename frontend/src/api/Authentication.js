import Future from "fluture";
import {prop} from "ramda";

import PathHandling from "./Utility/PathHandling";
import ResultHandling from "./Utility/ResponseHandling";

export default {
    /**
     * TODO: implement
     * Logs a user in.
     *
     * @param email
     * @param password
     * @return a Future.
     * @resolves with a sessionToken, if the credentials are valid.
     * @rejects with a reason, if the credentials are invalid or another error
     * occured.
     * @cancel
     */
    login: function (email, password) {
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;

            fetch(PathHandling.buildApiPath("/api/auth/login"), {
                "method": "POST",
                "mode": "cors",
                "data": JSON.stringify({
                    email,
                    password
                }),
                signal
            })
                .then(resolve)
                .catch(reject);

            return controller.abort;
        })
            .chain(ResultHandling.checkStatus(200))
            .chain(ResultHandling.extractJson)
            .map(prop("session_token"))
            .chainRej(ResultHandling.extractJson);
    },
    /**
     * TODO: implement
     * Logs the user with the given sessionToken out.
     *
     * @param sessionToken
     * @returns a Future.
     * @resolve with True, if everything went well.
     * @rejects with a reason, if an error occured.
     * @cancel
     */
    logout: function (sessionToken) {
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;

            fetch(PathHandling.buildApiPath("/api/auth/logout"), {
                "method": "GET",
                "mode": "cors",
                signal
            })
                .then(resolve)
                .catch(reject);

            return controller.abort;
        })
            .chain(ResultHandling.checkStatus(200))
            .chain(ResultHandling.extractJson)
            .map(() => true)
            .chainRej(ResultHandling.extractJson);
    },
    /**
     * TODO: implement
     * Checks, if a given sessionToken is valid.
     *
     * @param sessionToken
     * @returns a Future.
     * @resolves with True, if the sessionToken is valid.
     * @rejects with False, if the sessionToken is invalid.
     * @cancel
     */
    isSessionValid: function (sessionToken) {
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;

            fetch(PathHandling.buildApiPath(`/api/auth/${sessionToken}/isValid`), {
                "method": "GET",
                "mode": "cors",
                signal
            })
                .then(resolve)
                .catch(reject);

            return controller.abort;
        })
            .chain(ResultHandling.checkStatus(200))
            .chain(ResultHandling.extractJson)
            .map(prop("result"))
            .chainRej(ResultHandling.extractJson);
    }
}