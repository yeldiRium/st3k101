class Language {
    constructor(shortName, longName) {
        this.shortName = shortName;
        this.longName = longName;
    }

    /**
     * @param {Language} language
     * @return {Boolean}
     */
    equals(language) {
        return this.shortName == language.shortName
            && this.longName == language.longName;
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

    clone() {
        return new LanguageData(
            this.currentLanguage,
            this.originalLanguage,
            [...this.availableLanguages]
        );
    }
}

export default Language;

export {
    Language,
    LanguageData
}
