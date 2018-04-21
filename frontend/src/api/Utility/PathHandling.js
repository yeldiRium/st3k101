import config from "../../config";

import store from "../../store";

export default {
    /**
     * Constructs the full url to the requested API endpoint by prepending the
     * given path with the API url and adding potentially needed query parame-
     * ters conveying global state.
     *
     * Appends the language that is currently selected and stored in vuex.
     *
     * This is currently a bit verbose, since the Web API specification for URLs
     * (https://developer.mozilla.org/en-US/docs/Web/API/URL) does not yet allow
     * appending search parameters (at least not in nearly all browsers).
     * TODO: replace with API usage, once it is implemented more broadly.
     *
     * @param endpointPath An absolute path to an API endpoint.
     */
    buildApiPath: function (endpointPath) {
        let url = new URL(endpointPath, config.apiURL);
        let href = url.href;

        if (url.search == "") {
            href += "?";
        }
        href += `locale=${store.state.language.currentLanguage.short}`;

        return href;
    }
}
