import Future from "fluture";

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
        return Future.reject({
            reason: "Not implemented yet."
        });
    },
    /**
     * TODO: implement
     * Logs the user with the given sessionToken out.
     *
     * @param sessionToken
     * @returns a Future.
     * @resolve with a server reponse, if everything went well.
     * @rejects with a reason, if an error occured.
     * @cancel
     */
    logout: function (sessionToken) {
        return Future.reject({
            reason: "Not implemented yet."
        });
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
        return Future.reject({
            reason: "Not implemented yet."
        });
    }
}