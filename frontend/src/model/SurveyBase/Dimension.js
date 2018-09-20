import SurveyBase from "./SurveyBase";
import { clone, map } from "ramda";

class Dimension extends SurveyBase {
  /**
   * @param {string} href See Resource.
   * @param {String} id See Resource.
   * @param {Array<Party>} owners See OwnedResource.
   * @param {LanguageData} languageData See SurveyBase.
   * @param {Boolean} template See SurveyBase.
   * @param {String} referenceId See SurveyBase.
   * @param {string} name The Dimension's name.
   * @param {Array.<Question>} questions An Array of all connected Questions.
   * @param {boolean} randomizeQuestions Whether the Questions should be dis-
   *  played in a random order to DataSubjects.
   */
  constructor(
    href,
    id,
    owners,
    languageData,
    template,
    referenceId,
    name,
    questions,
    randomizeQuestions
  ) {
    super(href, id, owners, languageData, template, referenceId);
    this.name = name;
    this.questions = questions;
    this.randomizeQuestions = randomizeQuestions;
  }

  /**
   * True, if this Question is a ShadowQuestion.
   *
   * @returns {boolean}
   */
  get isShadow() {
    throw new Error("Please override this.");
  }

  /**
   * True, if this Question is a ConcreteQuestion.
   *
   * @returns {boolean}
   */
  get isConcrete() {
    throw new Error("Please override this.");
  }

  /**
   * @returns {Dimension}
   */
  clone() {
    return new Dimension(
      this._href,
      this._id,
      [...this._owners],
      this.languageData.clone(),
      this.template,
      this.name,
      map(clone, this.questions),
      this.randomizeQuestions
    );
  }
}

class ConcreteDimension extends Dimension {
  /**
   *
   * @param {string} href See Resource.
   * @param {String} id See Resource.
   * @param {Array<Party>} owners See OwnedResource.
   * @param {LanguageData} languageData See SurveyBase.
   * @param {Boolean} template See SurveyBase.
   * @param {String} referenceId See SurveyBase.
   * @param {string} name See Dimension.
   * @param {Array.<Question>} questions See Dimension.
   * @param {boolean} randomizeQuestions See Dimension.
   * @param {number}  incomingReferenceCount Number of references to this
   *  Dimension.
   *  This counts references not owned by the current user and can thus be
   *  bigger than the number of ownedIncomingReferences.
   * @param {Array.<Resource|ShadowDimension>} ownedIncomingReferences List of
   *  all references (in form of hrefs or ShadowDimension instances) to this
   *  Dimension, which the current user owns.
   */
  constructor(
    href,
    id,
    owners,
    languageData,
    template,
    referenceId,
    name,
    questions,
    randomizeQuestions,
    incomingReferenceCount,
    ownedIncomingReferences
  ) {
    super(
      href,
      id,
      owners,
      languageData,
      template,
      referenceId,
      name,
      questions,
      randomizeQuestions
    );

    this.incomingReferenceCount = incomingReferenceCount;
    this.ownedIncomingReferences = ownedIncomingReferences;
  }

  get isShadow() {
    return false;
  }

  get isConcrete() {
    return true;
  }

  /**
   * @returns {ConcreteDimension}
   */
  clone() {
    return new ConcreteDimension(
      this._href,
      this._id,
      [...this._owners],
      this.languageData.clone(),
      this.template,
      this.referenceId,
      this.name,
      map(clone, this.questions),
      this.randomizeQuestions,
      this.incomingReferenceCount,
      map(clone, this.ownedIncomingReferences)
    );
  }

  /**
   * Number of reference to this Dimension, which are owned by the current
   * user.
   *
   * @returns {number}
   */
  ownedIncomingReferenceCount() {
    return this.ownedIncomingReferences.length;
  }
}

class ShadowDimension extends Dimension {
  /**
   *
   * @param {string} href See Resource.
   * @param {String} id See Resource.
   * @param {Array<Party>} owners See OwnedResource.
   * @param {LanguageData} languageData See SurveyBase.
   * @param {String} referenceId See SurveyBase.
   * @param {string} name See Dimension.
   * @param {Array.<Question>} questions See Dimension.
   * @param {boolean} randomizeQuestions See Dimension.
   * @param {Resource|ConcreteDimension} referenceTo Href or instance of the
   *  referenced Dimension.
   */
  constructor(
    href,
    id,
    owners,
    languageData,
    referenceId,
    name,
    questions,
    randomizeQuestions,
    referenceTo
  ) {
    super(
      href,
      id,
      owners,
      languageData,
      false,
      referenceId,
      name,
      questions,
      randomizeQuestions
    );
    this.referenceTo = referenceTo;
  }

  get isShadow() {
    return true;
  }

  get isConcrete() {
    return false;
  }

  clone() {
    return new ShadowDimension(
      this._href,
      this._id,
      [...this._owners],
      this.languageData.clone(),
      this.referenceId,
      this.name,
      map(clone, this.questions),
      this.randomizeQuestions,
      this.referenceTo.clone()
    );
  }
}

export default Dimension;

export { Dimension, ConcreteDimension, ShadowDimension };
