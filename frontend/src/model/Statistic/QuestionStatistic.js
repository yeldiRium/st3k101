/**
 * Contains statistical data on a single Wuestion.
 */
class QuestionStatistic {
  /**
   * @param questionId {Integer}
   * @param questionHref {String}
   * @param questionText {String}
   * @param questionRangeStart {Integer}
   * @param questionRangeEnd {Integer}
   * @param n {Integer}
   * @param biggest {Integer}
   * @param smallest {Integer}
   * @param q1 {Number}
   * @param q2 {Number}
   * @param q3 {Number}
   */
  constructor(
    questionId,
    questionHref,
    questionText,
    questionRangeStart,
    questionRangeEnd,
    n,
    biggest,
    smallest,
    q1,
    q2,
    q3
  ) {
    this.questionId = questionId;
    this.questionHref = questionHref;
    this.questionText = questionText;
    this.questionRangeStart = questionRangeStart;
    this.questionRangeEnd = questionRangeEnd;
    this.n = n;
    this.biggest = biggest;
    this.smallest = smallest;
    this.q1 = q1;
    this.q2 = q2;
    this.q3 = q3;
  }

  /**
   * Checks if this is equal to other.
   *
   * @param other {QuestionStatistic}
   * @returns {boolean}
   */
  equals(other) {
    if (!other.hasOwnProperty("questionId")) {
      return false;
    }
    return this.questionId === other.questionId;
  }

  /**
   * Returns a deepcopy of this.
   *
   * @returns {QuestionStatistic}
   */
  clone() {
    return new QuestionStatistic(
      this.questionId,
      this.questionHref,
      this.questionText,
      this.questionRangeStart,
      this.questionRangeEnd,
      this.n,
      this.biggest,
      this.smallest,
      this.q1,
      this.q2,
      this.q3
    );
  }
}

export default QuestionStatistic;

export { QuestionStatistic };
