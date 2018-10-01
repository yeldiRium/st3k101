import * as R from "ramda";
import { allTrue } from "../utility/functional";

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
    return (
      this.shortName === language.shortName &&
      this.longName === language.longName
    );
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
    return new LanguageData(this.currentLanguage, this.originalLanguage, [
      ...this.availableLanguages
    ]);
  }

  /**
   * Strict equality check.
   *
   * @param {LanguageData} otherLanguageData
   * @returns {Boolean}
   */
  equals(otherLanguageData) {
    return R.allPass([
      o => R.equals(o.currentLanguage, this.currentLanguage),
      o => R.equals(o.originalLanguage, this.originalLanguage),
      o =>
        allTrue(
          R.zipWith(R.equals, o.availableLanguages, this.availableLanguages)
        )
    ])(otherLanguageData);
  }
}

const byShortName = R.ascend(R.prop("shortName"));

export default Language;

export { Language, LanguageData, byShortName };
