class Submission {
  constructor(questionnaire) {
    this._datasubjectEmail = "";
    this.password = "";
    this.captchaToken = "";
    this._dimensions = [];

    // deep copy dimension hierarchy of questionnaire
    for (let dimension of questionnaire.dimensions) {
      let questions = [];
      for (let question of dimension.questions) {
        questions.push({
          id: question.id,
          value: -1 // values that are not filled in are -1
        });
      }
      this._dimensions.push({
        id: dimension.id,
        questions: questions
      });
    }
  }

  set dataSubjectEmail(email) {
    this._datasubjectEmail = email;
  }

  get dataSubject() {
    return {
      email: this._datasubjectEmail
    };
  }

  get dimensions() {
    return this._dimensions;
  }

  updateValueForQuestionId(id, value) {
    for (let dimension of this._dimensions) {
      for (let question of dimension.questions) {
        if (question.id === id) {
          question.value = value;
        }
      }
    }
  }

  clone() {
    return new Submission({ dimensions: this._dimensions });
  }
}

export default Submission;

export { Submission };
