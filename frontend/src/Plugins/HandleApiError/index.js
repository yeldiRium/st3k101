import {is} from "ramda";

import store from "../../store";
import router from "../../router";

const Plugin = {
    install(Vue, options = {}) {
        /**
         * Makes sure that plugin can be installed only once
         */
        if (this.installed) {
            return
        }
        this.installed = true;

        /**
         * Checks which kind of error is passend and defines behaviour for each.
         *
         * This is tightly coupled to the rest of the application and is only
         * in a Plugin, because it needs to modify the Vue prototype.
         *
         * @param {ApiError} error
         */
        Vue.prototype.$handleApiError = function (error) {
            console.error(error);
            switch (error.name) {
                case "TypeError":
                    Vue.prototype.$notify({
                        type: "warn",
                        title: "Network error",
                        text: "You seem to be offline. Please check your connection and try again."
                    });
                    break;
                case "UnknownError":
                    Vue.prototype.$notify({
                        type: "warn",
                        title: "Unknown error",
                        text: "An unknown error has occured. Please try again. If this problem persists, start crying."
                    });
                    break;
                case "AuthorizationError":
                case "ForbiddenError":
                    store.commit("session/endSession");
                    router.push({name: "Authentication"});
                    console.log(this);
                    Vue.prototype.$notify({
                        type: "error",
                        title: "Session expired",
                        text: "Your session has expired. Please log in again."
                    });
                    break;
                case "BadRequestError":
                    Vue.prototype.$notify({
                        type: "error",
                        title: "Bad request",
                        text: "Some request data was bad. Check your logs."
                    });
                    break;
                case "ValidationError":
                    Vue.prototype.$notify({
                        type: "error",
                        title: "Validation error",
                        text: error.message
                    });
                    break;
                default:
                    Vue.prototype.$notify({
                        type: "warning",
                        title: "Maybe something went wrong",
                        text: "We're not soure though. If you experience any issues, go fuck yourself."
                    });
            }
        }
    }
};

export default Plugin;