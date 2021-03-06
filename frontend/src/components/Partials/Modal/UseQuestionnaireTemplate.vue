<template>
    <modal name="modal-use-questionnaire-template"
           height="auto"
           @before-open="beforeOpen"
           width="80%"
           :scrollable="true"
    >
        <div class="modal-use-questionnaire-template__header">
            use Questionnaire template
        </div>
        <div class="modal-use-questionnaire-template__body">
            <FuzzySearchableList :keys="searchableKeys"
                                 :items="questionnaireTemplates"
                                 v-on:item-clicked="use"
            >
            </FuzzySearchableList>
            <span
                    v-if="questionnaireTemplates.length === 0"
            >
                Keine Templates gefunden!
            </span>
            <Button @action="cancel">
                Cancel
            </Button>
        </div>
    </modal>
</template>

<script>
import { mapGetters } from "vuex-fluture";
import { isNil } from "ramda";

import Button from "../Form/Button";
import ClosableModal from "./ClosableModal";
import FuzzySearchableList from "../../Partials/List/FuzzySearchableList";

export default {
  name: "ModalUseQuestionnaireTemplate",
  extends: ClosableModal,
  components: {
    Button,
    FuzzySearchableList
  },
  data() {
    return {
      questionnaire: null,
      handler: null,
      searchableKeys: [
        { key: "name", display: "Name" },
        { key: "referenceId", display: "xAPI Activity ID" },
        { key: "description", display: "Description" }
      ]
    };
  },
  computed: {
    ...mapGetters("questionnaires", ["questionnaireTemplates"])
  },
  methods: {
    close() {
      this.cancel();
    },
    beforeOpen({ params: { handler } }) {
      if (isNil(handler)) {
        throw new Error("Parameter handler required!");
      }
      this.handler = handler;
    },
    cancel() {
      this.$modal.hide("modal-use-questionnaire-template");
    },
    /**
     * Emits a "questionnaire-create" event with all needed data to cre-
     * ate the questionnaire.
     */
    use(questionnaire) {
      this.$modal.hide("modal-use-questionnaire-template");
      this.handler({
        questionnaire
      });
    }
  }
};
</script>

<style lang="scss">
@import "../../scss/_variables";

.modal-use-questionnaire-template {
  display: grid;
  grid-template-rows: 2em auto 2em;
  grid-row-gap: 10px;

  &__header {
    background-color: $primary-light;

    font-size: 1.4em;
    text-align: center;
  }

  &__body {
    padding-top: 10px;
    padding-left: 20px;
    padding-right: 20px;

    display: flex;
    flex-flow: column;
    align-items: center;

    > * {
      margin-bottom: 10px;
    }
  }
}
</style>
