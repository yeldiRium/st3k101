import { is } from "ramda";

import store from "../../store";
import router from "../../router";

const Plugin = {
  install(Vue, options = {}) {
    /**
     * Makes sure that plugin can be installed only once
     */
    if (this.installed) {
      return;
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
    Vue.prototype.$handleApiError = function(error) {
      console.error(error);
      switch (error.name) {
        case "TypeError":
          Vue.prototype.$notify({
            type: "warn",
            title: "Network error",
            text:
              "You seem to be offline. Please check your connection and try again."
          });
          break;
        case "UnknownError":
          Vue.prototype.$notify({
            type: "warn",
            title: "Unknown error",
            text: "An unknown error has occured. Please try again."
          });
          break;
        case "ForbiddenError":
          Vue.prototype.$notify({
            type: "error",
            title: "Forbidden",
            text: "Some request was rejected. Check your logs."
          });
          break;
        case "AuthorizationError":
          store.commit("session/endSession");
          router.push({ name: "Authentication" });
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
        case "NotFoundError":
          Vue.prototype.$notify({
            type: "warn",
            title: "Page not found",
            text: "The page you were trying to access could not be found."
          });
          break;
        case "ConflictError":
          Vue.prototype.$notify({
            type: "error",
            title: "Conflicting data",
            text: "Some data on the server is conflicting with your request."
          });
          break;
        default:
          Vue.prototype.$notify({
            type: "warning",
            title: "Maybe something went wrong",
            text: "We're not sure though."
          });
      }
    };
  }
};

export default Plugin;
