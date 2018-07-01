import OwnedResource from "../OwnedResource";

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
    constructor(href,
                id,
                owners,
                languageData,
                template,
                referenceId) {
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
}

export default SurveyBase;

export {
    SurveyBase
}
