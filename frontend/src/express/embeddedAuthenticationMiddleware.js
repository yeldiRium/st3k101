import Future from "fluture";
import R from "ramda";

/**
 * Keys of required parameters.
 * Can't process embedded authentication if any of these is not present.
 *
 * @type {Array}
 */
const requiredParameters = [];

/**
 * @param {Object}
 * @return {Boolean} true, if the object contains all required keys.
 */
const hasAllRequiredParameters = R.allPass(
    R.map(
        R.has,
        requiredParameters
    )
);

/**
 * @param frontendPath Path to the frontend files.
 * @param req Express request.
 * @param res Express response.
 * @param next Callback for next middleware.
 */
const embeddedAuthenticationMiddleware = frontendPath => (req, res, next) => {
    console.log("starting middleware");
    if (!hasAllRequiredParameters(req.body)) {
        res.status(666);
        return res.send("Get fucked")
    }

    const frontendParams = {};

    return Future.node(done => fs.readFile(`${frontendPath}/index.html`, done))
        .map(R.replace(
            "/*LaunchParameterPlaceholderDontRemovePlox*/",
            `var launchParameters = ${JSON.stringify(frontendParams)};`
        ))
        .fork(
            /** @type {ApiError|TypeError} */
            error => {
                res.status(error.status);
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