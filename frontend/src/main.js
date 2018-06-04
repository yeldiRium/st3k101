// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from "vue";
import "vuetify/dist/vuetify.css";
import Vuetify from "vuetify";
import Vuex from "vuex";

import "abortcontroller-polyfill";

import App from "./components/App";
import router from "./router";
import { initialize as initializeStore } from "./store";
import store from "./store";

Vue.use(Vuex);

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
