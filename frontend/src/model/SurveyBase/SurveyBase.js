import OwnedResource from "../OwnedResource";
import * as R from "ramda";

class SurveyBase extends OwnedResource {
  /**
   * @param {string} href See Resource.
   * @param {String} id See Resource.
   * @param {Array<Party>} owners See OwnedResource.
   * @param {LanguageData} languageData Language information about
   *  the SurveyBase.
   * @param {Boolean} template Whether the SurveyBase may be used as a
   *  template.
   * @param {String} referenceId A unified referenceId for the resource.
   */
  constructor(href, id, owners, languageData, template, referenceId) {
    super(href, id, owners);

    this.languageData = languageData;
    this.template = template;
    this.referenceId = referenceId;
  }

  /**
   * @returns {SurveyBase}
   */
  clone() {
    return new SurveyBase(
      this._href,
      this._id,
      [...this._owners],
      this.languageData.clone(),
      this.template,
      this.referenceId
    );
  }

  /**
   * Recurse through object hierarchy and collect all SurveyBases
   * along the way. For a Questionnaire, this will return all
   * dimensions and all questions. For a dimension, this will
   * return all questions, for a question, this will return [].
   *
   * @returns {Array<SurveyBase>}
   */
  getAllChildren() {
    let ownChildren = [];
    if (this.hasOwnProperty("dimensions")) {
      ownChildren = this.dimensions;
    } else if (this.hasOwnProperty("questions")) {
      ownChildren = this.questions;
    }
    return ownChildren.concat(
      R.flatten(R.map(sb => sb.getAllChildren(), ownChildren))
    );
  }

  /***
   * Indicates whether a Concrete SurveyBase is a template or a real Concrete.
   * Templates do not include all fields present in Concrete instances,
   * this flag can be used to determine if all fields are present or not.
   *
   * @returns {boolean|Boolean}
   */
  get isReadonlyTemplate() {
    return this.owners.length === 0 && this.template;
  }
}

export default SurveyBase;

export { SurveyBase };
