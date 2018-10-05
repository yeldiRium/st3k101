import { fetchApi } from "./Util/Request";
import { extractJson } from "./Util/Response";
import * as R from "ramda";
import { parseDataSubject } from "./Util/Parse";

/**
 * Queries DataSubjects and returns all matches. Be sure to use %-syntax if you
 * want to use fuzzy matching. (E.g. %banana%)
 *
 * @param {String} authenticationToken
 * @param {String} email
 * @param {String} moodleUsername
 * @param {String} source The source tool consumer
 * @returns {Future}
 * @resolve {Array<DataSubject>}
 * @reject {ApiError}
 * @cancel
 */
function fetchDataSubjectsByQuery(
  authenticationToken,
  { email = null, moodleUsername = null, source = null }
) {
  let query = {};
  if (!R.isNil(email)) {
    query.email = email;
  }
  if (!R.isNil(moodleUsername)) {
    query.moodle_username = moodleUsername;
  }
  if (!R.isNil(source)) {
    query.source = source;
  }

  return fetchApi("/api/datasubject", {
    authenticationToken,
    method: "POST",
    body: JSON.stringify(query)
  })
    .chain(extractJson)
    .map(R.map(parseDataSubject));
}

/**
 * Deletes a DataSubject and all personal data for it.
 *
 * @param {String} authenticationToken
 * @param {String} id
 * @returns {Future}
 * @resolve
 * @reject {ApiError}
 * @cancel
 */
function forgetDataSubject(authenticationToken, { id }) {
  return fetchApi(`/api/datasubject/${id}`, {
    authenticationToken,
    method: "DELETE"
  }).chain(extractJson); // TODO: what to do with return value?
}

export { fetchDataSubjectsByQuery, forgetDataSubject };
