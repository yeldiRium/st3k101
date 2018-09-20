import { map, clone } from "ramda";

class SubmissionDimension {
  /**
   * A read-only Dimension that is used when submitting responses
   * @param id
   * @param href
   * @param name
   * @param randomizeQuestionOrder
   * @param languageData
   * @param {Array<SubmissionQuestion>} questions
   */
  constructor(id, href, name, randomizeQuestionOrder, languageData, questions) {
    this.id = id;
    this.href = href;
    this.name = name;
    this.randomizeQuestionOrder = randomizeQuestionOrder;
    this.languageData = languageData;
    this.questions = questions;
  }

  clone() {
    return new SubmissionDimension(
      this.id,
      this.href,
      this.name,
      this.randomizeQuestionOrder,
      this.languageData,
      map(clone, this.questions)
    );
  }

  /**
   * @param {SubmissionDimension} otherSubmissionDimension
   * @returns {boolean} true, if both have the same id
   */
  equals(otherSubmissionDimension) {
    return this.id === otherSubmissionDimension.id;
  }
}

export default SubmissionDimension;

export { SubmissionDimension };
