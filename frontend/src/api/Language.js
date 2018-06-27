import {map} from "ramda";

import {fetchApi} from "./Util/Request";
import {extractJson} from "./Util/Response";
import {parseLanguage} from "./Util/Parse";

/**
 * Fetches all available Languages on the server.
 *
 * @returns {Future}
 * @resolve {Array<Language>}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function fetchLanguages() {
    return fetchApi(
        "/api/language", {}
    )
        .chain(extractJson)
        .map(map(parseLanguage))
}

export {
    fetchLanguages
};
