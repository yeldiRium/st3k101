import {is} from "ramda";

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
         */
        Vue.prototype.$handleApiError = function (error) {
            if (is("AuthenticationError", error)) {

            }
        }
    }
};

export default Plugin;
