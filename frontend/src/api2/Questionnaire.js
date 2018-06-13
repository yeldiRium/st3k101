/**
 * Fetches the Questionnaire from the API in the requested language.
 * Updates all translatable information in place and updates the
 * `languageData` object.
 *
 * Should also check, if the list of availableLanguages has changed and
 * overwrite the old one.
 *
 * @param {Questionnaire} questionnaire
 * @param {Language} language
 * @return Future
 * @resolve with nothing, since the Questionnaire is updated in place
 * @reject with an API error message, if something went wrong
 * @cancel TODO: is this cancellable?
 */
function fetchTranslation(questionnaire, language) {
    // TODO: fetch translation from api
    // TODO: set languageData in questionnaire
    // TODO: set translated fields in questionnaire
    throw new Error("Please implement this.");
}

/**
 * Adds a new translation to the given Questionnaire in the given Language.
 *
 * Does not update the questionnaire! It has to be fetched in the new Language after-
 * wards, if required.
 *
 * @param {Questionnaire} questionnaire
 * @param {Language} language
 * @param {String} text
 * @return {Future}
 * @resolve with true
 * @reject with an API error message
 * @cancel TODO: is this cancellable?
 */
function addNewTranslation(questionnaire, language, {text}) {
    // TODO: add new translation via api
    throw new Error("Please implement this.");
}

export {
    fetchTranslation,
    addNewTranslation
};