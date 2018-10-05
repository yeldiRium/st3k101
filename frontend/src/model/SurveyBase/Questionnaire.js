import SurveyBase from "./SurveyBase";
import * as R from "ramda";
import { allContentsEqual } from "../../utility/functional";

class Questionnaire extends SurveyBase {
  /**
   * @param {string} href See Resource.
   * @param {String} id See Resource.
   * @param {Array<Party>} owners See OwnedResource.
   * @param {LanguageData} languageData See SurveyBase.
   * @param {Boolean} template See SurveyBase.
   * @param {String} referenceId See SurveyBase.
   * @param {string} name The Questionnaire's name.
   * @param {string} description A description for the Questionnaire.
   * @param {boolean} isPublic Whether the Questionnaire can be filled out and
   *  submitted.
   * @param {Boolean} acceptsSubmissions
   * @param {boolean} allowEmbedded Whether the Questionnaire can be used in
   *  embedded mode in alternate frontends.
   * @param {string} xapiTarget
   * @param ltiConsumerKey {String} Shared secret for embedding & lti launch
   * @param {Array<Dimension>} dimensions The Questionnaire's child dimen-
   *  sions.
   * @param {Array<Challenge>} challenges A list of Challenges
   */
  constructor(
    href,
    id,
    owners,
    languageData,
    template,
    referenceId,
    name,
    description,
    isPublic,
    acceptsSubmissions,
    allowEmbedded,
    xapiTarget,
    ltiConsumerKey,
    dimensions,
    challenges
  ) {
    super(href, id, owners, languageData, template, referenceId);

    this.name = name;
    this.description = description;
    this.isPublic = isPublic;
    this.acceptsSubmissions = acceptsSubmissions;
    this.allowEmbedded = allowEmbedded;
    this.xapiTarget = xapiTarget;
    this.ltiConsumerKey = ltiConsumerKey;
    this.dimensions = dimensions;
    this.challenges = challenges;
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
   * @returns {Questionnaire}
   */
  clone() {
    return new Questionnaire(
      this._href,
      this._id,
      this._owners,
      this.languageData.clone(),
      this.template,
      this.referenceId,
      this.name,
      this.description,
      this.isPublic,
      this.acceptsSubmissions,
      this.allowEmbedded,
      this.xapiTarget,
      this.ltiConsumerKey,
      R.map(R.clone, this.dimensions),
      R.map(R.clone, this.challenges)
    );
  }

  /**
   * Strict equality check that checks if all members if this are the same as the
   * members of otherQuestionnaire.
   *
   * @param {Questionnaire} otherQuestionnaire
   * @returns {Boolean}
   */
  contentEquals(otherQuestionnaire) {
    return R.allPass([
      o => R.equals(o.href, this.href),
      o => R.equals(o.languageData, this.languageData),
      o => R.equals(o.template, this.template),
      o => R.equals(o.referenceId, this.referenceId),
      o => R.equals(o.name, this.name),
      o => R.equals(o.description, this.description),
      o => R.equals(o.isPublic, this.isPublic),
      o => R.equals(o.acceptsSubmissions, this.acceptsSubmissions),
      o => R.equals(o.allowEmbedded, this.allowEmbedded),
      o => R.equals(o.xapiTarget, this.xapiTarget),
      o => R.equals(o.ltiConsumerKey, this.ltiConsumerKey),
      o => allContentsEqual(o.dimensions, this.dimensions)
      // TODO also check challenges. Not needed at the moment, as this is only used for reloading shadows and those don't need to reload the concrete challenges.
    ])(otherQuestionnaire);
  }
}

class ConcreteQuestionnaire extends Questionnaire {
  /**
   * @param {string} href See Resource.
   * @param {String} id See Resource.
   * @param {Array<Party>} owners See OwnedResource.
   * @param {LanguageData} languageData See SurveyBase.
   * @param {Boolean} template See SurveyBase.
   * @param {String} referenceId See SurveyBase.
   * @param {string} name See Questionnaire.
   * @param {string} description See Questionnaire.
   * @param {boolean} isPublic See Questionnaire.
   * @param {boolean} acceptsSubmissions
   * @param {boolean} allowEmbedded See Questionnaire.
   * @param {string} xapiTarget See Questionnaire.
   * @param ltiConsumerKey {String} See Questionnaire.
   * @param {Array<Dimension>} dimensions See Questionnaire.
   * @param {Array<Challenge>} challenges A list of Challenges
   * @param {number}  incomingReferenceCount Number of references to this
   *  Questionnaire.
   *  This counts references not owned by the current user and can thus be
   *  bigger than the number of ownedIncomingReferences.
   * @param {Array.<Resource|ShadowQuestionnaire>} ownedIncomingReferences
   *  List of all references (in form of hrefs or ShadowQuestionnaire instan-
   *  ces) to this Questionnaire, which the current user owns.
   */
  constructor(
    href,
    id,
    owners,
    languageData,
    template,
    referenceId,
    name,
    description,
    isPublic,
    acceptsSubmissions,
    allowEmbedded,
    xapiTarget,
    ltiConsumerKey,
    dimensions,
    challenges,
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
      description,
      isPublic,
      acceptsSubmissions,
      allowEmbedded,
      xapiTarget,
      ltiConsumerKey,
      dimensions,
      challenges
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
   * Number of reference to this Questionnaire, which are owned by the current
   * user.
   *
   * @returns {number}
   */
  ownedIncomingReferenceCount() {
    return this.ownedIncomingReferences.length;
  }

  /**
   * @returns {ConcreteQuestionnaire}
   */
  clone() {
    return new ConcreteQuestionnaire(
      this._href,
      this._id,
      this._owners,
      this.languageData.clone(),
      this.template,
      this.referenceId,
      this.name,
      this.description,
      this.isPublic,
      this.acceptsSubmissions,
      this.allowEmbedded,
      this.xapiTarget,
      this.ltiConsumerKey,
      R.map(R.clone, this.dimensions),
      R.map(R.clone, this.challenges),
      this.incomingReferenceCount,
      R.map(R.clone, this.ownedIncomingReferences)
    );
  }
}

class QuestionnaireTemplate extends Questionnaire {
  constructor(href, id, languageData, referenceId, name, description) {
    super(
      href,
      id,
      [],
      languageData,
      true,
      referenceId,
      name,
      description,
      false,
      false,
      false,
      "",
      "",
      [],
      []
    );
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
    return new QuestionnaireTemplate(
      this.href,
      this.id,
      this.languageData.clone(),
      this.referenceId,
      this.name,
      this.description
    );
  }
}

class ShadowQuestionnaire extends Questionnaire {
  /**
   * @param {string} href See Resource.
   * @param {String} id See Resource.
   * @param {Array<Party>} owners See OwnedResource.
   * @param {LanguageData} languageData See SurveyBase.
   * @param {String} referenceId See SurveyBase.
   * @param {string} name See Questionnaire.
   * @param {string} description See Questionnaire.
   * @param {boolean} isPublic See Questionnaire.
   * @param {boolean} acceptsSubmissions
   * @param {boolean} allowEmbedded See Questionnaire.
   * @param {string} xapiTarget See Questionnaire.
   * @param ltiConsumerKey {String} See Questionnaire.
   * @param {Array<Dimension>} dimensions See Questionnaire.
   * @param {Array<Challenge>} challenges A list of Challenges
   * @param {Resource|ConcreteQuestionnaire} referenceTo Href or instance of the re-
   *  ferenced Questionnaire.
   */
  constructor(
    href,
    id,
    owners,
    languageData,
    referenceId,
    name,
    description,
    isPublic,
    acceptsSubmissions,
    allowEmbedded,
    xapiTarget,
    ltiConsumerKey,
    dimensions,
    challenges,
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
      description,
      isPublic,
      acceptsSubmissions,
      allowEmbedded,
      xapiTarget,
      ltiConsumerKey,
      dimensions,
      challenges
    );

    this.referenceTo = referenceTo;
  }

  get isShadow() {
    return true;
  }

  get isConcrete() {
    return false;
  }

  /**
   * @returns {ShadowQuestionnaire}
   */
  clone() {
    return new ShadowQuestionnaire(
      this._href,
      this._id,
      [...this._owners],
      this.languageData.clone(),
      this.referenceId,
      this.name,
      this.description,
      this.isPublic,
      this.acceptsSubmissions,
      this.allowEmbedded,
      this.xapiTarget,
      this.ltiConsumerKey,
      R.map(R.clone, this.dimensions),
      R.map(R.clone, this.challenges),
      this.referenceTo.clone()
    );
  }
}

export default Questionnaire;

export {
  Questionnaire,
  ConcreteQuestionnaire,
  ShadowQuestionnaire,
  QuestionnaireTemplate
};
