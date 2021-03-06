import SurveyBase from "./SurveyBase";
import * as R from "ramda";
import { allContentsEqual } from "../../utility/functional";

class Dimension extends SurveyBase {
  /**
   * @param {string} href See Resource.
   * @param {String} id See Resource.
   * @param {Array<Party>} owners See OwnedResource.
   * @param {LanguageData} languageData See SurveyBase.
   * @param {Boolean} template See SurveyBase.
   * @param {String} referenceId See SurveyBase.
   * @param {string} name The Dimension's name.
   * @param {Integer} position The Dimension's position within the Questionnaire.
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
    position,
    questions,
    randomizeQuestions
  ) {
    super(href, id, owners, languageData, template, referenceId);
    this.name = name;
    this.position = position;
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
      this.referenceId,
      this.name,
      this.position,
      R.map(R.clone, this.questions),
      this.randomizeQuestions
    );
  }

  /**
   * Strict equality check that checks if all members of this are the same as
   * the members of otherDimension.
   *
   * @param {Dimension} otherDimension
   * @returns {bool}
   */
  contentEquals(otherDimension) {
    return R.allPass([
      o => R.equals(o.href, this.href),
      o => R.equals(o.languageData, this.languageData),
      o => R.equals(o.referenceId, this.referenceId),
      o => R.equals(o.template, this.template),
      o => R.equals(o.name, this.name),
      o => R.equals(o.position, this.position),
      o => R.equals(o.randomizeQuestions, this.randomizeQuestions),
      o => allContentsEqual(o.questions, this.questions)
    ])(otherDimension);
  }
}

class DimensionTemplate extends Dimension {
  constructor(href, id, languageData, referenceId, name) {
    super(href, id, [], languageData, true, referenceId, name, 0, [], false);
  }

  get isReadonlyTemplate() {
    return true;
  }

  get isShadow() {
    return false;
  }

  get isConcrete() {
    return false;
  }

  clone() {
    return new DimensionTemplate(
      this.href,
      this.id,
      this.languageData.clone(),
      this.referenceId,
      this.name
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
   * @param {Integer} position See Dimension.
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
    position,
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
      position,
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
      this.position,
      R.map(R.clone, this.questions),
      this.randomizeQuestions,
      this.incomingReferenceCount,
      R.map(R.clone, this.ownedIncomingReferences)
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
   * @param {Integer} position See Dimension.
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
    position,
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
      position,
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
      this.position,
      R.map(R.clone, this.questions),
      this.randomizeQuestions,
      this.referenceTo.clone()
    );
  }
}

export default Dimension;

export { Dimension, ConcreteDimension, ShadowDimension, DimensionTemplate };
