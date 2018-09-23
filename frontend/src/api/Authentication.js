import * as Future from "fluture/index.js";
import * as R from "ramda";
import { extractJson } from "./Util/Response";
import { parseDataClient } from "./Util/Parse";
import { fetchApi } from "./Util/Request";
import { InternalServerError } from "./Errors";

/**
 * Register a new DataClient.
 *
 * @param {String} email
 * @param {String} password
 * @return {Future}
 * @resolve {DataClient}
 * @reject {TypeError|ApiError}
 * @cancel see fetchApi
 */
function register(email, password) {
  return fetchApi("/api/dataclient", {
    method: "POST",
    body: JSON.stringify({
      email,
      password
    })
  })
    .chain(extractJson)
    .map(parseDataClient);
}

/**
 * Requests a Session Token for a DataClient.
 *
 * @param {String} email
 * @param {String} password
 * @return {Future}
 * @resolve {String} to session token.
 * @reject {TypeError|ApiError}
 * @cancel see fetchApi
 */
function requestSession(email, password) {
  return fetchApi("/api/session", {
    method: "POST",
    body: JSON.stringify({
      email,
      password
    })
  })
    .chain(extractJson)
    .map(R.prop("session_token"));
}

/**
 * Ends a Session.
 *
 * @param {String} authenticationToken
 * @return {Future}
 * @resolve {Boolean} to true
 * @reject {TypeError|ApiError}
 * @cancel see fetchApi
 */
function endSession(authenticationToken) {
  return fetchApi("/api/session", {
    method: "DELETE",
    authenticationToken
  }).map(() => true);
}

/**
 * Retrieves the currently logged in DataClient.
 * Obviously only works when authenticated.
 *
 * @param {String} authenticationToken
 * @return {Future}
 * @resolve {DataClient}
 * @reject {TypeError|ApiError}
 * @cancel see fetchApi
 */
function getCurrentDataClient(authenticationToken) {
  return fetchApi("/api/dataclient", {
    authenticationToken
  })
    .chain(extractJson)
    .map(parseDataClient);
}

/**
 * Prepares the backend for an LTI launch by validating if the launch is valid
 * and provisioning an user account if it doesn't exist yet.
 * @param consumerKey {String}
 * @param userId {String}
 * @param questionnaireId {String}
 * @param context_id {String}
 * @param context_label {String}
 * @param context_title {String}
 * @param launch_presentation_locale {String}
 * @param launch_presentation_return_url {String}
 * @param lis_person_contact_email_primary {String}
 * @param lis_person_name_family {String}
 * @param lis_person_name_full {String}
 * @param lis_person_name_given {String}
 * @param resource_link_description {String}
 * @param resource_link_title {String}
 * @param tool_consumer_info_product_family_code {String}
 * @param tool_consumer_info_version {String}
 * @param tool_consumer_instance_description {String}
 * @param tool_consumer_instance_guid {String}
 * @resolves {String} {String}
 * @rejects {ApiError|TypeError}
 */
function requestLtiSession(
  consumerKey,
  userId,
  questionnaireId,
  clientIp,
  {
    context_id = null,
    context_label = null,
    context_title = null,
    launch_presentation_locale = null,
    launch_presentation_return_url = null,
    lis_person_contact_email_primary = null,
    lis_person_name_family = null,
    lis_person_name_full = null,
    lis_person_name_given = null,
    resource_link_description = null,
    resource_link_title = null,
    tool_consumer_info_product_family_code = null,
    tool_consumer_info_version = null,
    tool_consumer_instance_description = null,
    tool_consumer_instance_guid = null
  }
) {
  let body = R.filter(R.complement(R.isNil), {
    user_id: userId,
    oauth_consumer_key: consumerKey,
    context_id: context_id,
    context_label: context_label,
    context_title: context_title,
    launch_presentation_locale: launch_presentation_locale,
    launch_presentation_return_url: launch_presentation_return_url,
    lis_person_contact_email_primary: lis_person_contact_email_primary,
    lis_person_name_family: lis_person_name_family,
    lis_person_name_full: lis_person_name_full,
    lis_person_name_given: lis_person_name_given,
    resource_link_description: resource_link_description,
    resource_link_title: resource_link_title,
    tool_consumer_info_product_family_code: tool_consumer_info_product_family_code,
    tool_consumer_info_version: tool_consumer_info_version,
    tool_consumer_instance_description: tool_consumer_instance_description,
    tool_consumer_instance_guid: tool_consumer_instance_guid
  });
  // TODO: make hard-coded path configurable
  return fetchApi(`/api/questionnaire/${questionnaireId}/lti`, {
    method: "POST",
    headers: {
      "X-Forwarded-For": clientIp
    },
    body: JSON.stringify(body)
  })
    .chain(extractJson)
    .chain(
      R.ifElse(
        R.has("session_token"),
        R.pipe(
          R.prop("session_token"),
          Future.of
        ),
        () =>
          Future.reject(
            new InternalServerError(
              "Session token wasn't returned, although no error message was given."
            )
          )
      )
    );
}

export {
  register,
  requestSession,
  endSession,
  getCurrentDataClient,
  requestLtiSession
};
