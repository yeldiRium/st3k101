import OwnedResource from "../OwnedResource";

class SurveyBase extends OwnedResource {
    /**
     * @param {string} href See Resource.
     * @param {String} id See Resource.
     * @param {Party} owner See OwnedResource.
     * @param {LanguageData} languageData Language information about
     *  the SurveyBase.
     */
    constructor(href,
                id,
                owner, languageData) {
        super(href, id, owner);

        this.languageData = languageData;
    }
}

export default SurveyBase;

export {
    SurveyBase
}