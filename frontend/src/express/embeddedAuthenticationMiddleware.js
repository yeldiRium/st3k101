import R from "ramda";

import {getCurrentDataClient} from "../api/Authentication";

/**
 * @param req Express request.
 * @param res Express response.
 * @param next Callback for next middleware.
 */
const embeddedAuthenticationMiddleware = function (req, res, next) {
    // No key given, no access granted.
    if (req.method === "POST" && R.has("key", req.body)) {
        const key = req.body.key;

        return getCurrentDataClient(key).fork(
            error => {
                console.error(error);
                next();
            },
            /** @type {DataClient} */
            dataClient => {
                // A successful request means that the key is valid.
                // TODO: set cookie with key for the frontend.
                next();
            }
        );
    }
    next();
};

export default embeddedAuthenticationMiddleware;