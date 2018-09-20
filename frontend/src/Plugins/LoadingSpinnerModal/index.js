import Future from "fluture";
import vModal from "vue-js-modal";

import LoadingSpinnerModal from "./LoadingSpinnerModal";

const Plugin = {
  install(Vue, options = {}) {
    Vue.use(vModal);

    /**
     * Makes sure that plugin can be insstalled only once
     */
    if (this.installed) {
      return;
    }
    this.installed = true;

    /**
     * Starts the LoadingModal, executes the Future and closes the LoadingModal,
     * after the Future has resolved/rejected.
     * @param {Future} future
     * @return {Future}
     * @resolve depends on future
     * @reject depends on future
     * @cancel depends on future
     */
    Vue.prototype.$load = function(future) {
      return Future((reject, resolve) => {
        Vue.prototype.$modal.show("loading");
        resolve();
      })
        .chain(() => future)
        .mapRej(result => {
          Vue.prototype.$modal.hide("loading");
          return result;
        })
        .map(result => {
          Vue.prototype.$modal.hide("loading");
          return result;
        });
    };

    /**
     * Add Modal component.
     */
    Vue.component("LoadingSpinnerModal", LoadingSpinnerModal);
  }
};

export default Plugin;
