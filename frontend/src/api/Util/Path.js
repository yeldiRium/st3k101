import config from "../../config";
import { isNil, test } from "ramda";

const isAbsolutePath = path =>
  test(/^(https?:\/\/[^\s:\/]+(:\d{0,5})?)(\S+)$/, path);

/**
 * Returns a url to the API.
 *
 * @param {String} relativePath has to begin with a "/".
 * @param {Language} language
 * @returns {string}
 */
function buildApiUrl(relativePath, language = null) {
  let absolutePath = relativePath;
  if (!isAbsolutePath(relativePath)) {
    absolutePath = config.apiURL + relativePath;
  }
  if (isNil(language)) {
    return absolutePath;
  } else {
    if (test(/\?/, absolutePath)) {
      return absolutePath + `&locale=${language.shortName}`;
    } else {
      return absolutePath + `?locale=${language.shortName}`;
    }
  }
}

export { buildApiUrl };
