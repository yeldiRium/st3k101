// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from "vue";
import Vuex from "vuex";
import vClickOutside from "v-click-outside";

import "abortcontroller-polyfill";

import App from "./components/App";
import router from "./router";
import { initialize as initializeStore } from "./store";
import store from "./store";

Vue.use(Vuex);
Vue.use(vClickOutside);

Vue.config.productionTip = false;

initializeStore().fork(
    error => {
        store.commit("initialLoadingError", error);
    },
    data => {
        store.commit("initialLoadingDone", data);
    }
);

// TODO: remove these three lines. These register a fake DataClient for testing
// purposes.
import DataClient from "./model/DataClient";
store.commit("session/startSession", {sessionToken: "randomSessionToken"});
store.commit("session/setDataClient", {dataClient: new DataClient("randomHref", "a@b.c", "de")});

new Vue({
    el: "#container",
    router,
    store,
    components: {App},
    template: "<App/>"
});
