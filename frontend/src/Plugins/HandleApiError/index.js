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
            switch (error.name) {
                case "AuthenticationError":
                    store.commit("session/endSession");
                    router.push({name: "Authentication"});
                    console.log(this);
                    Vue.prototype.$notify({
                        type: "error",
                        title: "Session expired",
                        text: "Your session has expired. Please log in again."
                    });
                    break;
                default:
                    return;
            }
        }
    }
};

export default Plugin;
