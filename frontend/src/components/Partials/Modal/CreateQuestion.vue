<template>
    <modal name="modal-create-question"
           height="auto"
           @before-open="beforeOpen"
    >
        <CreateResource
                @cancel="cancel"
                @create="create"
        >
            <template slot="header">
                Create new Question
            </template>
            <template slot="body">
                <input class="modal-create-question__question-text"
                       name="question-text"
                       v-model="text"
                />
                <RangeEditor v-model="range"/>
            </template>
        </CreateResource>
    </modal>
</template>

<script>
import { isNil } from "ramda";
import { Range } from "../../../model/SurveyBase/Config/Range";

import CreateResource from "./CreateResource";
import RangeEditor from "../SurveyBase/Config/RangeEditor";
import ClosableModal from "./ClosableModal";

export default {
  name: "ModalCreateQuestion",
  extends: ClosableModal,
  components: {
    CreateResource,
    RangeEditor
  },
  data() {
    return {
      language: null,
      handler: null,
      text: "Question text",
      range: null
    };
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
      this.range = new Range({ end: 10 });
    },
    cancel() {
      this.$modal.hide("modal-create-question");
    },
    /**
     * Emits a "question-create" event with all data needed to create a
     * new Question.
     */
    create() {
      this.$modal.hide("modal-create-question");
      this.handler({
        text: this.text,
        range: this.range
      });
    }
  }
};
</script>

<style lang="scss">
.modal-create-question {
  &__question-text {
    width: 80%;
  }
}
</style>
