import config from "../../config";

/**
 * Returns a url to the API.
 *
 * @param {String} relativePath has to begin with a "/".
 * @returns {string}
 */
function buildApiUrl(relativePath) {
    return config.apiURL + relativePath;
}

export {
    buildApiUrl
};