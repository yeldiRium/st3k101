import OwnedResource from "./OwnedResource";

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

    /**
     * Fetches the SurveyBase from the API with the requested language.
     * Updates all translatable information in place and updates the
     * `languageData` object.
     *
     * Should also check, if the list of availableLanguages has changed and
     * overwrite the old one.
     *
     * @param language
     * @return Future
     * @resolve with nothing, since the SurveyBase is updated in place
     * @reject with an API error message, if something went wrong
     * @cancel TODO: is this cancellable?
     */
    fetchTranslation(language) {
        this.languageData.currentLanguage = language;
        throw new Error("Please implement this!");
    }
}

export default SurveyBase;

export {
    SurveyBase
}