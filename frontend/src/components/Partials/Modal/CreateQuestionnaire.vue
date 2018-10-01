<template>
    <modal name="modal-create-questionnaire"
           height="auto"
           @before-open="beforeOpen"
    >
        <CreateResource
                @cancel="cancel"
                @create="create"
        >
            <template slot="header">
                Create new Questionnaire
            </template>
            <template slot="body">
                    <LanguagePicker
                                class="modal-create-questionnaire__language-picker"
                            :language-data="languageData"
                            @choose-language="changeLanguage"
                            :useLongNames="true"
                    >
                    </LanguagePicker>

                    <input class="modal-create-questionnaire__questionnaire-name"
                           name="questionnaire-name"
                           v-model="name"
                    />

                <textarea v-model="description"/>

                <Toggle v-model="isPublic">
                    <template slot="off">
                        locked
                    </template>
                    <template slot="on">
                        published
                    </template>
                </Toggle>

                <Toggle v-model="allowEmbedded">
                    <template slot="off">
                        only in browser
                    </template>
                    <template slot="on">
                        allow embedding
                    </template>
                </Toggle>

                <label>
                    xAPI endpoint:
                    <input v-model="xapiTarget"/>
                </label>
            </template>
        </CreateResource>
    </modal>
</template>

<script>
import { isNil } from "ramda";
import { mapState } from "vuex-fluture";

import CreateResource from "./CreateResource";
import Toggle from "../Form/ToggleButton";
import ClosableModal from "./ClosableModal";
import LanguagePicker from "../LanguagePicker";
import { LanguageData } from "../../../model/Language";

export default {
  name: "ModalCreateQuestionnaire",
  extends: ClosableModal,
  components: {
    CreateResource,
    Toggle,
    LanguagePicker
  },
  data() {
    return {
      language: null,
      handler: null,
      name: "Questionnaire name",
      description: "Questionnaire description",
      isPublic: false,
      allowEmbedded: false,
      xapiTarget: ""
    };
  },
  computed: {
    ...mapState("session", ["dataClient"]),
    ...mapState("language", ["languages", "currentLanguage"]),
    languageData() {
      return new LanguageData(this.language, null, this.languages);
    }
  },
  methods: {
    close() {
      this.cancel();
    },
    beforeOpen({ params: { language, handler } }) {
      if (isNil(language)) {
        throw new Error("Parameter language required!");
      }
      if (isNil(handler)) {
        throw new Error("Parameter handler required!");
      }
      this.language = language;
      this.handler = handler;
    },
    changeLanguage(language) {
      this.language = language;
    },
    cancel() {
      this.$modal.hide("modal-create-questionnaire");
    },
    /**
     * Emits a "questionnaire-create" event with all needed data to cre-
     * ate the questionnaire.
     */
    create() {
      this.$modal.hide("modal-create-questionnaire");
      this.handler({
        name: this.name,
        description: this.description,
        isPublic: this.isPublic,
        allowEmbedded: this.allowEmbedded,
        xapiTarget: this.xapiTarget,
        language: this.language
      });
    }
  }
};
</script>

<style lang="scss">
.modal-create-questionnaire {
  &__questionnaire-name {
    width: 80%;
  }
}
</style>
