import config from "../../config";
import {isNil, test} from "ramda";

/**
 * Returns a url to the API.
 *
 * @param {String} relativePath has to begin with a "/".
 * @param {Language} language
 * @returns {string}
 */
function buildApiUrl(relativePath, language = null) {
    if (isNil(language)) {
        return config.apiURL + relativePath;
    } else {
        if (test(/\?/, relativePath)) {
            return config.apiURL + relativePath + `&locale=${language.shortName}`;
        } else {
            return config.apiURL + relativePath + `?locale=${language.shortName}`;
        }
    }
}

export {
    buildApiUrl
};
