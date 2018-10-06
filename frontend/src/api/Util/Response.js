import * as Future from "fluture/index.js";
import {
  ForbiddenError,
  BadRequestError,
  ConflictError,
  NotFoundError,
  UnknownError,
  AuthorizationError,
  InternalServerError
} from "../Errors";

/**
 * Returns the full initial response, if the status code is ok
 * (200 <= status < 300).
 *
 * Otherwise returns an Error object based on the status code.
 *
 * @param {Response} response
 * @return {Future} categorized response
 * @resolve {Response} with the original response, if it was ok
 * @reject {Error} with an error object, depending on the status code
 */
function categorizeResponse(response) {
  if (response.status >= 200 && response.status < 300) {
    return Future.of(response);
  }

  switch (response.status) {
    case 400:
      return Future.tryP(() => response.json()).chain(data =>
        Future.reject(new BadRequestError("Bad request.", data))
      );
    case 401:
      return Future.reject(new AuthorizationError("Not authorized."));
    case 403:
      return Future.reject(new ForbiddenError("Forbidden."));
    case 404:
      return Future.reject(new NotFoundError("Resource not found."));
    case 409:
      return Future.tryP(() => response.json()).chain(data =>
        Future.reject(new ConflictError("Conflicting data.", data))
      );
    case 500:
      return Future.reject(new InternalServerError("Internal server error."));
    default:
      return Future.tryP(() => response.json()).chain(data =>
        Future.reject(new UnknownError("Conflicting data.", data))
      );
  }
}

/**
 * Extracts the JSON content from a response.
 *
 * @param {Response} response
 * @returns a Future.
 * @resolves with the Response's JSON content.
 * @reject see response.json()
 */
const extractJson = function(response) {
  return Future.tryP(() => response.json());
};

/**
 * Extracts the JSON content and the content-language from a response.
 *
 * @param {Response} response
 * @returns {Future}.
 * @resolves with the Response's JSON content and content-language.
 * @rejects see response.json()
 */
const extractJsonPlusLanguage = function(response) {
  return Future.tryP(() => response.json()).map(data => ({
    data: data,
    language: response.headers.get("Content-Language")
  }));
};

export { categorizeResponse, extractJson, extractJsonPlusLanguage };
