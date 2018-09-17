const fs = require("fs");

import Future from "fluture";
import R from "ramda";
import {requestLtiSession} from "../api/Authentication";

/**
 * Keys of required parameters.
 * Can't process embedded authentication if any of these is not present.
 *
 * @type {Object}
 */
const requiredParameters = {
    "lti_message_type": "basic-lti-launch-request",
    "lti_version": "LTI-1p0",
    "oauth_consumer_key": null,
    "oauth_callback": "about:blank",
    "oauth_nonce": null,
    "oauth_signature": null,
    "oauth_signature_method": "HMAC-SHA1",
    "oauth_timestamp": null,
    "oauth_version": "1.0",
    "resource_link_id": null,
    "roles": null,
    "user_id": null
};

/**
 * @param {Object}
 * @return {Boolean} true, if the object contains all required keys.
 */
const hasAllRequiredParameters = R.allPass(
    R.map(
        R.has,
        Object.keys(requiredParameters)
    )
);


const hasValidParameters = R.allPass(
    R.map(
        (key, value) => requiredParameters[key] === value,
        R.filter(
            (_, value) => !R.isNil(value),
            Object.entries(requiredParameters)
        )
    )
);

/**
 * @param frontendPath Path to the frontend files.
 * @param req Express request.
 * @param res Express response.
 * @param next Callback for next middleware.
 */
const embeddedAuthenticationMiddleware = frontendPath => (req, res, next) => {
    if (!hasAllRequiredParameters(req.body) || !hasValidParameters(req.body)) {
        res.status(400);
        return res.send("Not a valid LTI launch request.");
    }

    let cancel = requestLtiSession(
        req.body.oauth_consumer_key,
        req.body.user_id,
        req.params.questionnaireId,
        req.body
    )
        .chain(
            res => Future.node(done => fs.readFile(`${frontendPath}/index.html`, done))
                .chain(res => Future.of(res.toString()))
                .map(
                    R.replace(
                        "/*LaunchParameterPlaceholderDontRemovePlox*/",
                        `var ltiSessionToken = ${JSON.stringify(res)};`
                    )
                )
        )
        .fork(
        /** @type {ApiError} */
            error => {
                let status = (error.status >= 100 && error.status < 600)? error.status : 500;
                res.status(status);
                res.send(error.message);
                next();
            },
            processedHtml => {
                res.status(200);
                res.send(processedHtml);
                next();
            }
        );
};

export default embeddedAuthenticationMiddleware;