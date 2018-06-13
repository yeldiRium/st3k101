import OwnedResource from "../OwnedResource";

class SurveyBase extends OwnedResource {
    /**
     * @param {string} href See Resource.
     * @param {Party} owner See OwnedResource.
     * @param {LanguageData} languageData Language information about
     *  the SurveyBase.
     */
    constructor(href,
                owner,
                languageData) {
        super(href, owner);

        this.languageData = languageData;
    }
}

export default SurveyBase;

export {
    SurveyBase
}