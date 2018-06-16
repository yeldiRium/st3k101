import Language from "../../model/Language";
import DataClient from "../../model/DataClient";

/**
 * Parses the common API representation of a language into a Language instance.
 *
 * @param {String} name
 * @param {String} value
 * @return {Language}
 */
function parseLanguage({name, value}) {
    return new Language(name, value);
}

/**
 * Parses the common API representation of a DataClient into a DataClient in-
 * stance.
 *
 * TODO: set href correctly, once outputs it
 *
 * @param {String} email
 * @param {Number} id
 * @param {Object} language
 * @return {DataClient}
 */
function parseDataClient({email, id, language}) {
    return new DataClient(
        "href" + id,
        email,
        parseLanguage(language)
    );
}

export {
    parseLanguage,
    parseDataClient
};