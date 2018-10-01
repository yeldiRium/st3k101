<template>
    <modal name="modal-use-question-template"
           height="auto"
           @before-open="beforeOpen"
           :scrollable="true"
    >
        <div class="modal-use-question-template__header">
            use Question template
        </div>
        <div class="modal-use-question-template__body">
            <FuzzySearchableList :keys="searchableKeys"
                                 :items="questionTemplates"
                                 v-on:item-clicked="use"
            >
            </FuzzySearchableList>
            <span
                    v-if="questionTemplates.length === 0"
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
import FuzzySearchableList from "../List/FuzzySearchableList";

export default {
  name: "ModalUseQuestionTemplate",
  components: {
    FuzzySearchableList,
    Button
  },
  data() {
    return {
      question: null,
      handler: null,
      searchableKeys: [
        { key: "text", display: "Text" },
        { key: "referenceId", display: "xAPI Activity ID" }
      ]
    };
  },
  computed: {
    ...mapGetters("questions", ["questionTemplates"])
  },
  methods: {
    beforeOpen({ params: { handler } }) {
      if (isNil(handler)) {
        throw new Error("Parameter handler required!");
      }
      this.handler = handler;
    },
    cancel() {
      this.$modal.hide("modal-use-question-template");
    },
    /**
     * Emits a "question-create" event with all needed data to cre-
     * ate the question.
     */
    use(question) {
      this.$modal.hide("modal-use-question-template");
      this.handler({
        question
      });
    }
  }
};
</script>

<style lang="scss">
@import "../../scss/_variables";

.modal-use-question-template {
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
