// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from "vue";
import Vuex from "vuex";
import vClickOutside from "v-click-outside";
import vNotification from "vue-notification";
import vModal from "vue-js-modal";
import vLoading from "./Plugins/LoadingSpinnerModal";
import vApiError from "./Plugins/HandleApiError";

import "abortcontroller-polyfill";

import App from "./components/App";
import router from "./router";
import { initialize as initializeStore } from "./store";
import store from "./store";

Vue.use(Vuex);
Vue.use(vClickOutside);
Vue.use(vNotification);
Vue.use(vModal);
Vue.use(vLoading);
Vue.use(vApiError);

Vue.config.productionTip = false;

initializeStore().fork(
    error => {
        store.commit("initialLoadingError", error);
    },
    data => {
        store.commit("initialLoadingDone", data);
    }
);

new Vue({
    el: "#container",
    router,
    store,
    components: {App},
    template: "<App/>"
});
