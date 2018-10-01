<template>
    <modal name="modal-translate-question"
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
                <input class="modal-translate-question__question-text"
                       text="question-text"
                       v-model="text"
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
  text: "ModalTranslateQuestion",
  extends: ClosableModal,
  components: {
    TranslateResource,
    Toggle
  },
  data() {
    return {
      language: null,
      handler: null,
      text: null
    };
  },
  computed: {
    ...mapState("session", ["dataClient"]),
    headerText() {
      const longName = toLower(propOr("", "longName", this.language));
      return `Translate Question into ${longName}`;
    }
  },
  methods: {
    close() {
      this.cancel();
    },
    beforeOpen({ params: { language, handler, text } }) {
      if (isNil(language)) {
        throw new Error("Parameter language required!");
      }
      if (isNil(handler)) {
        throw new Error("Parameter handler required!");
      }
      if (isNil(text)) {
        throw new Error("Parameter text required!");
      }
      this.language = language;
      this.handler = handler;
      this.text = text;
    },
    cancel() {
      this.$modal.hide("modal-translate-question");
    },
    /**
     * Emits a "question-translate" event with all needed data to
     * translate the question.
     */
    translate() {
      this.$modal.hide("modal-translate-question");
      this.handler({
        language: this.language,
        text: this.text
      });
    }
  }
};
</script>

<style lang="scss">
.modal-translate-question {
  &__question-text {
    width: 80%;
  }
}
</style>
