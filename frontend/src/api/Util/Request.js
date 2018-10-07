import { isNil } from "ramda";
import * as Future from "fluture/index.js";

import { buildApiUrl } from "./Path";
import { categorizeResponse } from "./Response";

/**
 * Build headers from a given authentication token.
 *
 * @param {String} authenticationToken
 * @returns {Object}
 */
function buildAuthenticationHeaders(authenticationToken = "") {
  if (authenticationToken !== "") {
    return {
      Authorization: `Bearer ${authenticationToken}`
    };
  } else {
    return {};
  }
}

const defaultHeaders = {
  "Content-Type": "application/json"
};

/**
 * Fetches a resource with added behaviour.
 *
 * This is tightly coupled to the used vuex store, since it reads the currently
 * logged in DataClient's sessionToken for authentication purposes.
 * It also updates the SessionTokenCookie, if an authenticated request was
 * successful.
 *
 * Also pre-parses the result and categorizes errors.
 *
 * @param {String} path
 * @param {String} method
 * @param {String} body
 * @param {Object<String>} headers
 * @param {String} authenticationToken
 * @param {Language} language
 *
 * @return {Future}
 * @resolve {Response}
 * @reject {TypeError|ApiError} TypeError on network error, for the rest see
 *      categorizeResponse.
 * @cancel cancels the http request
 */
function fetchApi(
  path,
  {
    method = "GET",
    body = "",
    headers = {},
    authenticationToken = "",
    language = null
  }
) {
  return Future.Future((reject, resolve) => {
    const controller = new AbortController();
    const signal = controller.signal;

    const useHeaders = {
      ...defaultHeaders,
      ...headers,
      ...buildAuthenticationHeaders(authenticationToken)
    };

    const fetchParams = {
      method,
      headers: useHeaders,
      signal
    };

    if (method !== "GET" && method !== "HEAD") {
      fetchParams["body"] = body;
    }

    fetch(buildApiUrl(path, language), fetchParams)
      .then(resolve)
      .catch(reject);

    return controller.abort;
  }).chain(categorizeResponse);
}

export { fetchApi };
