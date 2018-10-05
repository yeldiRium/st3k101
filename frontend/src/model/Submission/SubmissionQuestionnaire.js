import { map, clone } from "ramda";

class SubmissionQuestionnaire {
  /**
   * A read-only Questionnaire that is used when submitting responses.
   * It lacks some fields of the full Questionnaire class and thus has
   * it's own model class.
   * @param id
   * @param href
   * @param name
   * @param description
   * @param languageData
   * @param passwordEnabled
   * @param acceptsSubmissions
   * @param {Array<SubmissionDimension>} dimensions
   */
  constructor(
    id,
    href,
    name,
    description,
    languageData,
    passwordEnabled,
    acceptsSubmissions,
    dimensions
  ) {
    this.id = id;
    this.href = href;
    this.name = name;
    this.description = description;
    this.languageData = languageData;
    this.passwordEnabled = passwordEnabled;
    this.acceptsSubmissions = acceptsSubmissions;
    this.dimensions = dimensions;
  }

  clone() {
    return new SubmissionQuestionnaire(
      this.id,
      this.href,
      this.name,
      this.description,
      this.languageData,
      this.passwordEnabled,
      this.acceptsSubmissions,
      map(clone, this.dimensions)
    );
  }

  /**
   * @param {SubmissionQuestionnaire} otherSubmissionQuestionnaire
   * @returns {boolean} true, if both have the same id
   */
  equals(otherSubmissionQuestionnaire) {
    return this.id === otherSubmissionQuestionnaire.id;
  }
}

export default SubmissionQuestionnaire;

export { SubmissionQuestionnaire };
