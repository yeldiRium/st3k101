class LanguageData {
    /**
     * Each in short version.
     *
     * @param {string} currentLanguage
     * @param {string} originalLanguage
     * @param {Array.<string>} availableLanguages
     */
    constructor(currentLanguage, originalLanguage, availableLanguages) {
        this.currentLanguage = currentLanguage;
        this.originalLanguage = originalLanguage;
        this.availableLanguages = availableLanguages;
    }
}

export default LanguageData;