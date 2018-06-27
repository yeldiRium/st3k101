import {configure} from '@storybook/vue'

import Vue from "vue";
import Vuex from "vuex-fluture";
import vClickOutside from "v-click-outside";
import vNotification from "vue-notification";
import vModal from "vue-js-modal";
import vLoading from "../src/Plugins/LoadingSpinnerModal";
import vApiError from "../src/Plugins/HandleApiError";

Vue.use(Vuex);
Vue.use(vClickOutside);
Vue.use(vNotification);
Vue.use(vModal);
Vue.use(vLoading);
Vue.use(vApiError);

function loadStories() {
    require('../src/stories')
}

configure(loadStories, module);
