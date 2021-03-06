<template>
    <modal name="modal-translate-dimension"
           height="auto"
           @before-open="beforeOpen"
    >
        <TranslateResource
                @cancel="cancel"
                @translate="translate"
        >
            <template slot="header">
                {{ headerText }}
            </template>
            <template slot="body">
                <input class="modal-translate-dimension__dimension-name"
                       name="dimension-name"
                       v-model="name"
                />
            </template>
        </TranslateResource>
    </modal>
</template>

<script>
import { isNil, propOr, toLower } from "ramda";
import { mapState } from "vuex-fluture";

import TranslateResource from "./TranslateResource";
import Toggle from "../Form/ToggleButton";
import ClosableModal from "./ClosableModal";

export default {
  name: "ModalTranslateDimension",
  extends: ClosableModal,
  components: {
    TranslateResource,
    Toggle
  },
  data() {
    return {
      language: null,
      handler: null,
      name: null
    };
  },
  computed: {
    ...mapState("session", ["dataClient"]),
    headerText() {
      const longName = toLower(propOr("", "longName", this.language));
      return `Translate Dimension into ${longName}`;
    }
  },
  methods: {
    close() {
      this.cancel();
    },
    beforeOpen({ params: { language, handler, name } }) {
      if (isNil(language)) {
        throw new Error("Parameter language required!");
      }
      if (isNil(handler)) {
        throw new Error("Parameter handler required!");
      }
      if (isNil(name)) {
        throw new Error("Parameter name required!");
      }
      this.language = language;
      this.handler = handler;
      this.name = name;
    },
    cancel() {
      this.$modal.hide("modal-translate-dimension");
    },
    /**
     * Emits a "dimension-translate" event with all needed data to
     * translate the dimension.
     */
    translate() {
      this.$modal.hide("modal-translate-dimension");
      this.handler({
        language: this.language,
        name: this.name
      });
    }
  }
};
</script>

<style lang="scss">
.modal-translate-dimension {
  &__dimension-name {
    width: 80%;
  }
}
</style>
