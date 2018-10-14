import { map, prop } from "ramda";

import { Language, LanguageData } from "../../model/Language";
import DataClient from "../../model/DataClient";
import Range from "../../model/SurveyBase/Config/Range";
import {
  ConcreteQuestionnaire,
  QuestionnaireTemplate,
  ShadowQuestionnaire
} from "../../model/SurveyBase/Questionnaire";
import {
  ConcreteDimension,
  DimensionTemplate,
  ShadowDimension
} from "../../model/SurveyBase/Dimension";
import {
  ConcreteQuestion,
  ShadowQuestion
} from "../../model/SurveyBase/Question";
import { Resource } from "../../model/Resource";
import EMailWhitelist from "../../model/SurveyBase/Challenge/EMailWhitelist";
import EMailBlacklist from "../../model/SurveyBase/Challenge/EMailBlacklist";
import Password from "../../model/SurveyBase/Challenge/Password";
import {
  ItemAddedTrackerEntry,
  ItemRemovedTrackerEntry,
  QuestionnaireRemovedTrackerEntry,
  TranslatedPropertyUpdatedTrackerEntry,
  PropertyUpdatedTrackerEntry
} from "../../model/TrackerEntry";
import SubmissionQuestionnaire from "../../model/Submission/SubmissionQuestionnaire";
import SubmissionDimension from "../../model/Submission/SubmissionDimension";
import SubmissionQuestion from "../../model/Submission/SubmissionQuestion";
import QuestionStatistic from "../../model/Statistic/QuestionStatistic";
import DataSubject from "../../model/DataSubject";
import { ValidationError } from "../Errors";

/**
 * Parses the API representation of a Language into a Language object.
 *
 * @param {String} item_id
 * @param {String} value
 * @throws {ValidationError} when a required parameter is missing or invalid.
 * @return {Language}
 */
function parseLanguage({ item_id, value }) {
  if (item_id === undefined) {
    throw new ValidationError("Field `item_id` is required..");
  }
  if (value === undefined) {
    throw new ValidationError("Field `value` is required..");
  }
  return new Language(item_id, value);
}

/**
 * Parses the three language components usually contained in any translatable
 * object in the API into a LanguageData object.
 *
 * @param current_language
 * @param original_language
 * @param available_languages
 * @return {LanguageData}
 */
function parseLanguageData({
  current_language,
  original_language,
  available_languages
}) {
  return new LanguageData(
    parseLanguage(current_language),
    parseLanguage(original_language),
    map(parseLanguage, available_languages)
  );
}

/**
 * Parses a simple resource.
 *
 * @param {String} href
 * @param {String} id
 * @returns {Resource}
 */
function parseResource({ href, id }) {
  return new Resource(href, id);
}

/**
 * Parses an array of DataClient Roles.
 *
 * @param {Array<Object>} roles
 * @returns {Array<Roles>}
 */
function parseRoles(roles) {
  return map(prop("value"), roles);
}

/**
 * Parses the common API representation of a DataClient into a DataClient in-
 * stance.
 *
 * @param {String} email
 * @param {Number} id
 * @param {String} href
 * @param {Object} language
 * @param {Array<Object>} roles
 * @return {DataClient}
 */
function parseDataClient({ email, id, href, language, roles }) {
  return new DataClient(
    href,
    id,
    email,
    parseLanguage(language),
    parseRoles(roles)
  );
}

/**
 * Parses the anonymized API representation of a DataClient.
 *
 * @param id
 * @param href
 * @return {DataClient}
 */
function parseSmallDataClient({ id, href }) {
  return new DataClient(href, id, "", null, []);
}

/**
 * Parses the full API representation of a DataSubject.
 *
 * @param {String} id
 * @param {String} email
 * @param {String} lti_user_id
 * @param {String} moodle_username
 * @param {String} source
 * @returns {DataSubject}
 */
function parseDataSubject({ id, email, lti_user_id, moodle_username, source }) {
  return new DataSubject(id, email, lti_user_id, moodle_username, source);
}

/**
 * Parses all challenges present in the given data into an array of Challenges.
 *
 * TODO: add more Challenges
 *
 * @param {Object} questionnaire A API representation of a Questionnaire.
 * @return {Array<Challenge>}
 */
function parseChallenges(questionnaire) {
  return [
    parseEMailWhitelistChallenge(questionnaire),
    parseEmailBlacklistChallenge(questionnaire),
    parsePasswordChallenge(questionnaire)
  ];
}

/**
 * Parses the EMailWhitelist Challenge.
 *
 * @param {Boolean} email_whitelist_enabled
 * @param {Array<String>} email_whitelist
 * @returns {EMailWhitelist}
 */
function parseEMailWhitelistChallenge({
  email_whitelist_enabled,
  email_whitelist
}) {
  return new EMailWhitelist(email_whitelist_enabled, email_whitelist);
}

/**
 * Parses the EMailBlacklist Challenge.
 *
 * @param {Boolean} email_blacklist_enabled
 * @param {Array<String>} email_blacklist
 * @returns {EMailBlacklist}
 */
function parseEmailBlacklistChallenge({
  email_blacklist_enabled,
  email_blacklist
}) {
  return new EMailBlacklist(email_blacklist_enabled, email_blacklist);
}

/**
 * Parses the Password Challenge.
 *
 * @param {Boolean} password_enabled
 * @param {String} password
 * @returns {Password}
 */

function parsePasswordChallenge({ password_enabled, password }) {
  return new Password(password_enabled, password);
}

/**
 * Parses the common API representation of a Questionnaire and recognizes, whe-
 * ther it is a ShadowQuestionnaire or a ConcreteQuestionnaire.
 *
 * @param {Object} data
 * @return {Questionnaire}
 */
function parseQuestionnaire(data) {
  if (prop("shadow", data) === true) {
    return parseShadowQuestionnaire(data, data); // TODO use ...rest
  } else if (!data.hasOwnProperty("dimensions")) {
    return parseTemplateQuestionnaire(data);
  }
  return parseConcreteQuestionnaire(data, data); // TODO use ...rest
}

/**
 * Parses the common API representation of a Questionnaire that is a template
 * and is not owned by the current user. In this case, some information will
 * be stripped by the API and we need to replace it with default values here.
 *
 * @param {String} href
 * @param {String} id
 * @param {String} reference_id
 * @param {String} name
 * @param {String} description
 * @param {Array<Dimension>} dimensions
 * @param {Boolean} template
 * @param {Language} current_language
 * @param {Language} original_language
 * @param {Array<Language>} available_languages
 * @returns {QuestionnaireTemplate}
 */
function parseTemplateQuestionnaire({
  href,
  id,
  reference_id,
  name,
  description,
  current_language,
  original_language,
  available_languages
}) {
  return new QuestionnaireTemplate(
    href,
    id,
    parseLanguageData({
      current_language,
      original_language,
      available_languages
    }),
    reference_id,
    name,
    description
  );
}

/**
 * Parses the common API representation of a ShadowQuestionnaire.
 *
 * @param {String} href
 * @param {String} id
 * @param {Array} owners
 * @param {String} reference_id
 * @param {String} name
 * @param {String} description
 * @param {Array} dimensions
 * @param {Boolean} published
 * @param {Boolean} accepts_submissions
 * @param {Boolean} template
 * @param {Boolean} allow_embedded
 * @param {String} xapi_target
 * @param {String} lti_consumer_key
 * @param {Object} current_language
 * @param {Object} original_language
 * @param {Array} available_languages
 * @param {Object} reference_to
 * @param {Object} whole The whole thing again, but not destructured
 *
 * @return {ShadowQuestionnaire}
 */
function parseShadowQuestionnaire(
  {
    href,
    id,
    owners,
    reference_id,
    name,
    description,
    dimensions,
    published,
    accepts_submissions,
    allow_embedded,
    xapi_target,
    lti_consumer_key,
    current_language,
    original_language,
    available_languages,
    reference_to
  },
  whole
) {
  return new ShadowQuestionnaire(
    href,
    id,
    map(parseSmallDataClient, owners),
    parseLanguageData({
      current_language,
      original_language,
      available_languages
    }),
    reference_id,
    name,
    description,
    published,
    accepts_submissions,
    allow_embedded,
    xapi_target,
    lti_consumer_key,
    map(parseDimension, dimensions),
    parseChallenges(whole),
    parseResource(reference_to)
  );
}

/**
 * Parses the common API representation of a ConcreteQuestionnaire.
 *
 * @param {String} href
 * @param {String} id
 * @param {Array} owners
 * @param {String} reference_id
 * @param {String} name
 * @param {String} description
 * @param {Array} dimensions
 * @param {Boolean} published
 * @param {Boolean} accepts_submissions
 * @param {Boolean} template
 * @param {Boolean} allow_embedded
 * @param {String} xapi_target
 * @param {String} lti_consumer_key
 * @param {Object} current_language
 * @param {Object} original_language
 * @param {Array} available_languages
 * @param {Array} owned_incoming_references
 * @param {Number} incoming_reference_count
 * @param {Object} whole The whole thing again, but not destructured
 *
 * @return {ConcreteQuestionnaire}
 */
function parseConcreteQuestionnaire(
  {
    href,
    id,
    owners,
    reference_id,
    name,
    description,
    dimensions,
    published,
    accepts_submissions,
    template,
    allow_embedded,
    xapi_target,
    lti_consumer_key,
    current_language,
    original_language,
    available_languages,
    owned_incoming_references,
    incoming_reference_count
  },
  whole
) {
  return new ConcreteQuestionnaire(
    href,
    id,
    map(parseSmallDataClient, owners),
    parseLanguageData({
      current_language,
      original_language,
      available_languages
    }),
    template,
    reference_id,
    name,
    description,
    published,
    accepts_submissions,
    allow_embedded,
    xapi_target,
    lti_consumer_key,
    map(parseDimension, dimensions),
    parseChallenges(whole),
    incoming_reference_count,
    map(parseResource, owned_incoming_references)
  );
}

/**
 * Parses the common API representation of a Dimension and recognizes, whe-
 * ther it is a ShadowDimension or a ConcreteDimension.
 *
 * @param {Object} data
 * @return {Dimension}
 */
function parseDimension(data) {
  if (prop("shadow", data) === true) {
    return parseShadowDimension(data);
  } else if (!data.hasOwnProperty("questions")) {
    return parseTemplateDimension(data);
  }
  return parseConcreteDimension(data);
}

/**
 * Parses the common API representation of a Dimension that is a template
 * and is not owned by the current user. In this case, some information will
 * be stripped by the API and we need to replace it with default values here.
 *
 * @param {String} href
 * @param {String} id
 * @param {String} reference_id
 * @param {String} name
 * @param {Array<Question>} questions
 * @param {Boolean} randomize_question_order
 * @param {Boolean} template
 * @param {Language} current_language
 * @param {Language} original_language
 * @param {Array<Language>} available_languages
 * @returns {DimensionTemplate}
 */
function parseTemplateDimension({
  href,
  id,
  reference_id,
  name,
  randomize_question_order,
  template,
  current_language,
  original_language,
  available_languages
}) {
  return new DimensionTemplate(
    href,
    id,
    parseLanguageData({
      current_language,
      original_language,
      available_languages
    }),
    reference_id,
    name
  );
}

/**
 * Parses the common API representation of a ShadowDimension.
 *
 * @param {String} href
 * @param {String} id
 * @param {Array} owners
 * @param {String} reference_id
 * @param {String} name
 * @param {Integer} position
 * @param {Array} questions
 * @param {Boolean} randomize_question_order
 * @param {Boolean} template
 * @param {Object} current_language
 * @param {Object} original_language
 * @param {Array} available_languages
 * @param {Object} reference_to
 *
 * @return {ShadowDimension}
 */
function parseShadowDimension({
  href,
  id,
  owners,
  reference_id,
  name,
  position,
  questions,
  randomize_question_order,
  current_language,
  original_language,
  available_languages,
  reference_to
}) {
  return new ShadowDimension(
    href,
    id,
    map(parseSmallDataClient, owners),
    parseLanguageData({
      current_language,
      original_language,
      available_languages
    }),
    reference_id,
    name,
    position,
    map(parseQuestion, questions),
    randomize_question_order,
    parseResource(reference_to)
  );
}

/**
 * Parses the common API representation of a ConcreteQuestionnaire.
 *
 * @param {String} href
 * @param {String} id
 * @param {Array} owners
 * @param {String} reference_id
 * @param {String} name
 * @param {Integer} position
 * @param {Array} questions
 * @param {Boolean} randomize_question_order
 * @param {Boolean} template
 * @param {Object} current_language
 * @param {Object} original_language
 * @param {Array} available_languages
 * @param {Array} owned_incoming_references
 * @param {Number} incoming_reference_count
 *
 * @return {ConcreteDimension}
 */
function parseConcreteDimension({
  href,
  id,
  owners,
  reference_id,
  name,
  position,
  questions,
  randomize_question_order,
  template,
  current_language,
  original_language,
  available_languages,
  owned_incoming_references,
  incoming_reference_count
}) {
  return new ConcreteDimension(
    href,
    id,
    map(parseSmallDataClient, owners),
    parseLanguageData({
      current_language,
      original_language,
      available_languages
    }),
    template,
    reference_id,
    name,
    position,
    map(parseQuestion, questions),
    randomize_question_order,
    incoming_reference_count,
    map(parseResource, owned_incoming_references)
  );
}

/**
 * Parses the common API representation of a Question and recognizes, whe-
 * ther it is a ShadowQuestion or a ConcreteQuestion.
 *
 * @param {Object} data
 * @return {Question}
 */
function parseQuestion(data) {
  if (prop("shadow", data) === true) {
    return parseShadowQuestion(data);
  } else if (!data.hasOwnProperty("owners")) {
    return parseTemplateQuestion(data);
  }
  return parseConcreteQuestion(data);
}

/**
 * Parses the common API representation of a Question that is a template
 * and is not owned by the current user. In this case, some information will
 * be stripped by the API and we need to replace it with default values here.
 *
 * @param {String} href
 * @param {String} id
 * @param {String} reference_id
 * @param {String} text
 * @param {Integer} range_start
 * @param {Integer} range_end
 * @param range_start_label
 * @param range_end_label
 * @param {Boolean} template
 * @param {Language} current_language
 * @param {Language} original_language
 * @param {Array<Language>} available_languages
 * @returns {ConcreteQuestion}
 */
function parseTemplateQuestion({
  href,
  id,
  reference_id,
  text,
  range_start,
  range_end,
  range_start_label,
  range_end_label,
  template,
  current_language,
  original_language,
  available_languages
}) {
  // TODO: template Question class
  return new ConcreteQuestion(
    href,
    id,
    [],
    parseLanguageData({
      current_language,
      original_language,
      available_languages
    }),
    template,
    reference_id,
    text,
    0,
    new Range({
      start: range_start,
      end: range_end,
      startLabel: range_start_label,
      endLabel: range_end_label
    }),
    0,
    []
  );
}

/**
 * Parses the common API representation of a ShadowQuestion.
 *
 * @param {String} href
 * @param {String} id
 * @param {Array} owners
 * @param {String} reference_id
 * @param {String} text
 * @param {Integer} position
 * @param {Number} range_start
 * @param {Number} range_end
 * @param {Boolean} template
 * @param {Object} current_language
 * @param {Object} original_language
 * @param {Array} available_languages
 * @param {Object} reference_to
 *
 * @return {ShadowQuestion}
 */
function parseShadowQuestion({
  href,
  id,
  owners,
  reference_id,
  text,
  position,
  range_start,
  range_end,
  range_start_label,
  range_end_label,
  current_language,
  original_language,
  available_languages,
  reference_to
}) {
  return new ShadowQuestion(
    href,
    id,
    map(parseSmallDataClient, owners),
    parseLanguageData({
      current_language,
      original_language,
      available_languages
    }),
    reference_id,
    text,
    position,
    new Range({
      start: range_start,
      end: range_end,
      startLabel: range_start_label,
      endLabel: range_end_label
    }),
    parseResource(reference_to)
  );
}

/**
 * Parses the common API representation of a ConcreteQuestionnaire.
 *
 * @param {String} href
 * @param {String} id
 * @param {Array} owners
 * @param {String} reference_id
 * @param {String} text
 * @param {Integer} position
 * @param {Number} range_start
 * @param {Number} range_end
 * @param {String} range_start_label
 * @param {String} range_end_label
 * @param {Boolean} template
 * @param {Object} current_language
 * @param {Object} original_language
 * @param {Array} available_languages
 * @param {Array} owned_incoming_references
 * @param {Number} incoming_reference_count
 *
 * @return {ConcreteQuestion}
 */
function parseConcreteQuestion({
  href,
  id,
  owners,
  reference_id,
  text,
  position,
  range_start,
  range_end,
  range_start_label,
  range_end_label,
  template,
  current_language,
  original_language,
  available_languages,
  owned_incoming_references,
  incoming_reference_count
}) {
  return new ConcreteQuestion(
    href,
    id,
    map(parseSmallDataClient, owners),
    parseLanguageData({
      current_language,
      original_language,
      available_languages
    }),
    template,
    reference_id,
    text,
    position,
    new Range({
      start: range_start,
      end: range_end,
      startLabel: range_start_label,
      endLabel: range_end_label
    }),
    incoming_reference_count,
    map(parseResource, owned_incoming_references)
  );
}

/**
 * Parses the common API representation of a PropertyUpdatedTrackerEntry.
 *
 * @param dataclient_email {String}
 * @param timestamp {Date}
 * @param item_name {String}
 * @param item_type {String}
 * @param item_href {String}
 * @param property_name {String}
 * @param previous_value {String}
 * @param new_value {String}
 * @returns {PropertyUpdatedTrackerEntry}
 */
function parsePropertyUpdatedTrackerEntry({
  dataclient_email,
  timestamp,
  item_name,
  item_type,
  item_href,
  property_name,
  previous_value,
  new_value
}) {
  return new PropertyUpdatedTrackerEntry(
    dataclient_email,
    timestamp,
    item_name,
    item_type,
    item_href,
    property_name,
    previous_value,
    new_value
  );
}

/**
 * Parses the common API representation of a TranslatedPropertyUpdatedTrackerEntry.
 *
 * @param dataclient_email {String}
 * @param timestamp {Date}
 * @param item_name {String}
 * @param item_type {String}
 * @param item_href {String}
 * @param property_name {String}
 * @param previous_value {String}
 * @param new_value {String}
 * @param language {Language}
 * @returns {TranslatedPropertyUpdatedTrackerEntry}
 */
function parseTranslatedPropertyUpdatedTrackerEntry({
  dataclient_email,
  timestamp,
  item_name,
  item_type,
  item_href,
  property_name,
  previous_value,
  new_value,
  language
}) {
  return new TranslatedPropertyUpdatedTrackerEntry(
    dataclient_email,
    timestamp,
    item_name,
    item_type,
    item_href,
    property_name,
    previous_value,
    new_value,
    language
  );
}

/**
 * Parses the common API representation of an ItemAddedTrackerEntry.
 * @param dataclient_email {String}
 * @param timestamp {Date}
 * @param parent_item_name {String}
 * @param parent_item_type {String}
 * @param parent_item_href {String}
 * @param added_item_name {String}
 * @param added_item_type {String}
 * @param added_item_href {String}
 * @returns {ItemAddedTrackerEntry}
 */
function parseItemAddedTrackeEntry({
  dataclient_email,
  timestamp,
  parent_item_name,
  parent_item_type,
  parent_item_href,
  added_item_name,
  added_item_type,
  added_item_href
}) {
  return new ItemAddedTrackerEntry(
    dataclient_email,
    timestamp,
    parent_item_name,
    parent_item_type,
    parent_item_href,
    added_item_name,
    added_item_type,
    added_item_href
  );
}

/**
 * Parses the common API representation of an ItemRemovedTrackerEntry.
 * @param dataclient_email {String}
 * @param timestamp {Date}
 * @param parent_item_name {String}
 * @param parent_item_type {String}
 * @param parent_item_href {String}
 * @param removed_item_name {String}
 * @returns {ItemRemovedTrackerEntry}
 */
function parseItemRemovedTrackerEntry({
  dataclient_email,
  timestamp,
  parent_item_name,
  parent_item_type,
  parent_item_href,
  removed_item_name
}) {
  return new ItemRemovedTrackerEntry(
    dataclient_email,
    timestamp,
    parent_item_name,
    parent_item_type,
    parent_item_href,
    removed_item_name
  );
}

/**
 * Parses the common API representation of a QuestionnaireRemovedTrackerEntry.
 * @param dataclient_email {String}
 * @param timestamp {Date}
 * @param questionnaire_name {String}
 * @returns {QuestionnaireRemovedTrackerEntry}
 */
function parseQuestionnaireRemovedTrackerEntry({
  dataclient_email,
  timestamp,
  questionnaire_name
}) {
  return new QuestionnaireRemovedTrackerEntry(
    dataclient_email,
    timestamp,
    questionnaire_name
  );
}

/**
 * Parses the common API representations of all kinds of TrackerEntries.
 * @param data {Object}
 * @returns {*}
 */
function parseTrackerEntry(data) {
  switch (data.type) {
    case "PropertyUpdatedTrackerEntry":
      return parsePropertyUpdatedTrackerEntry(data);
    case "TranslatedPropertyUpdatedTrackerEntry":
      return parseTranslatedPropertyUpdatedTrackerEntry(data);
    case "ItemAddedTrackerEntry":
      return parseItemAddedTrackeEntry(data);
    case "ItemRemovedTrackerEntry":
      return parseItemRemovedTrackerEntry(data);
    case "QuestionnaireRemovedTrackerEntry":
      return parseQuestionnaireRemovedTrackerEntry(data);
  }
}

/**
 * Parses a single Question of the common API representation of a
 * SubmissionQuestionnaire.
 *
 * @param id {Integer}
 * @param href {String}
 * @param text {String}
 * @param range_start {Integer}
 * @param range_end {Integer}
 * @param range_start_label {String}
 * @param range_end_label {String}
 * @param current_language {Language}
 * @param original_language {Language}
 * @param available_languages {Array<Language>}
 * @returns {SubmissionQuestion}
 */
function parseSubmissionQuestion({
  id,
  href,
  text,
  range_start,
  range_end,
  range_start_label,
  range_end_label,
  current_language,
  original_language,
  available_languages
}) {
  return new SubmissionQuestion(
    id,
    href,
    text,
    new Range({
      start: range_start,
      end: range_end,
      startLabel: range_start_label,
      endLabel: range_end_label
    }),
    parseLanguageData({
      current_language,
      original_language,
      available_languages
    })
  );
}

/**
 * Parses a single Dimension of the common API representation of a
 * SubmissionQuestionnaire.
 *
 * @param id {Integer}
 * @param href {String}
 * @param name {String}
 * @param randomize_question_order {Boolean}
 * @param current_language {Language}
 * @param original_language {Language}
 * @param available_languages {Array<Language>}
 * @param questions {Array<Object>}
 * @returns {SubmissionDimension}
 */
function parseSubmissionDimension({
  id,
  href,
  name,
  randomize_question_order,
  current_language,
  original_language,
  available_languages,
  questions
}) {
  return new SubmissionDimension(
    id,
    href,
    name,
    randomize_question_order,
    parseLanguageData({
      current_language,
      original_language,
      available_languages
    }),
    map(parseSubmissionQuestion, questions)
  );
}

/**
 * Parses the common API representation of a SubmissionQuestionnaire.
 *
 * @param id {Integer}
 * @param href {String}
 * @param name {String}
 * @param description {String}
 * @param password_enabled {Boolean}
 * @param accepts_submissions
 * @param dimensions {Array<Object>}
 * @param current_language {Language}
 * @param original_language {Language}
 * @param available_languages {Array<Language>}
 * @returns {SubmissionQuestionnaire}
 */
function parseSubmissionQuestionnaire({
  id,
  href,
  name,
  description,
  password_enabled,
  accepts_submissions,
  dimensions,
  current_language,
  original_language,
  available_languages
}) {
  return new SubmissionQuestionnaire(
    id,
    href,
    name,
    description,
    parseLanguageData({
      current_language,
      original_language,
      available_languages
    }),
    password_enabled,
    accepts_submissions,
    map(parseSubmissionDimension, dimensions)
  );
}

/**
 * Parses the common API representation of a QuestionStatistic.
 *
 * @param question_id {Integer}
 * @param question_href {String}
 * @param question_text {String}
 * @param question_range_start {Integer}
 * @param question_range_end {Integer}
 * @param n {Integer}
 * @param biggest {Integer}
 * @param smallest {Integer}
 * @param q1 {Number}
 * @param q2 {Number}
 * @param q3 {Number}
 * @returns {QuestionStatistic}
 */
function parseQuestionStatistic({
  question_id,
  question_href,
  question_text,
  question_range_start,
  question_range_end,
  n,
  biggest,
  smallest,
  q1,
  q2,
  q3
}) {
  return new QuestionStatistic(
    question_id,
    question_href,
    question_text,
    question_range_start,
    question_range_end,
    n,
    biggest,
    smallest,
    q1,
    q2,
    q3
  );
}

export {
  parseLanguage,
  parseLanguageData,
  parseDataClient,
  parseDataSubject,
  parseChallenges,
  parseEMailWhitelistChallenge,
  parseEmailBlacklistChallenge,
  parsePasswordChallenge,
  parseQuestionnaire,
  parseTemplateQuestionnaire,
  parseShadowQuestionnaire,
  parseConcreteQuestionnaire,
  parseDimension,
  parseShadowDimension,
  parseConcreteDimension,
  parseQuestion,
  parseShadowQuestion,
  parseConcreteQuestion,
  parseTrackerEntry,
  parseSubmissionQuestionnaire,
  parseQuestionStatistic
};
