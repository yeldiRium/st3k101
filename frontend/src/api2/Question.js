/**
 * Fetches the Question from the API in the requested language.
 * Updates all translatable information in place and updates the
 * `languageData` object.
 *
 * Should also check, if the list of availableLanguages has changed and
 * overwrite the old one.
 *
 * @param {Question} question
 * @param {Language} language
 * @return {Future}
 * @resolve with nothing, since the Question is updated in place
 * @reject with an API error message
 * @cancel TODO: is this cancellable?
 */
function fetchTranslation(question, language) {
    // TODO: fetch translation from api
    // TODO: set languageData in question
    // TODO: set translated fields in question
    throw new Error("Please implement this.");
}

/**
 * Adds a new translation to the given Question in the given Language.
 *
 * Does not update the question! It has to be fetched in the new Language after-
 * wards, if required.
 *
 * @param {Question} question
 * @param {Language} language
 * @param {String} text
 * @return {Future}
 * @resolve with true
 * @reject with an API error message
 * @cancel TODO: is this cancellable?
 */
function addNewTranslation(question, language, {text}) {
    // TODO: add new translation via api
    throw new Error("Please implement this.");
}

export {
    fetchTranslation,
    addNewTranslation
};