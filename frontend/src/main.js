// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from "vue";
import {App} from "./app";
import router from "./router";
import store from "./store";

import "vuetify/dist/vuetify.css";

import Vuetify from "vuetify";

Vue.use(Vuetify);

Vue.config.productionTip = false;

window.bus = new Vue();

new Vue({
    el: "#container",
    router,
    store,
    components: {App},
    template: "<App/>"
});


fetch("http://localhost:1337/api/locales", {
    "method": "GET",
    "mode": "cors"
}).then(console.log).catch(console.error);