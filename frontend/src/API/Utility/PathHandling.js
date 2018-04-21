import config from "../../config";

export default {
    /**
     * Constructs the full url to the requested API endpoint by prepending the
     * given path with the API url and adding potentially needed query parame-
     * ters conveying global state.
     *
     * Currently no additional query parameters are added; In the future this
     * could be used to e.g. handle locale requesting.
     *
     * @param endpointPath An absolute path to an API endpoint.
     */
    "buildApiPathTo": function (endpointPath) {
        return config.apiURL + endpointPath
    }
}
