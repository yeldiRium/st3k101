import OwnedResource from "../OwnedResource";

class SurveyBase extends OwnedResource {
    /**
     * @param {string} href See Resource.
     * @param {String} id See Resource.
     * @param {Array<Party>} owners See OwnedResource.
     * @param {LanguageData} languageData Language information about
     *  the SurveyBase.
     */
    constructor(href,
                id,
                owners, languageData) {
        super(href, id, owners);

        this.languageData = languageData;
    }
}

export default SurveyBase;

export {
    SurveyBase
}
