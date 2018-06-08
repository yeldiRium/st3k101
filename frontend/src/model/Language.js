class Language {
    constructor(shortName, longName) {
        this.shortName = shortName;
        this.longName = longName;
    }
}

class LanguageData {
    /**
     * Each in short version.
     *
     * @param {Language} currentLanguage
     * @param {Language} originalLanguage
     * @param {Array.<Language>} availableLanguages
     */
    constructor(currentLanguage, originalLanguage, availableLanguages) {
        this.currentLanguage = currentLanguage;
        this.originalLanguage = originalLanguage;
        this.availableLanguages = availableLanguages;
    }
}

export default Language;

export {
    Language,
    LanguageData
}