import { isNil, test } from "ramda";

/**
 * Returns a url to the API.
 *
 * @param {String} path has to begin with a "/".
 * @param {Language} language
 * @returns {string}
 */
function buildApiUrl(path, language = null) {
  if (isNil(language)) {
    return path;
  } else {
    if (test(/\?/, path)) {
      return path + `&locale=${language.shortName}`;
    } else {
      return path + `?locale=${language.shortName}`;
    }
  }
}

export { buildApiUrl };
