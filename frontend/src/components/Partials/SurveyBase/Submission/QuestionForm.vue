<template>
    <div class="question-form">
        <div class="question-form__header">
            {{ question.text }}
        </div>
        <div class="question-form__body">
            <Range :range="question.range"
                   :preview="false"
                   @selector-change="updateResponse($event)"
            />
        </div>
    </div>
</template>

<script>
import Range from "../Config/RangeSVG";

export default {
  name: "QuestionForm",
  props: {
    question: null
  },
  components: {
    Range
  },
  methods: {
    updateResponse(value) {
      this.$emit("response-change", {
        questionId: this.question.id,
        value: value
      });
    }
  }
};
</script>

<style lang="scss">
@import "../../../scss/variables";
.question-form {
  border-bottom: $lighter 1px dotted;
  &__header {
    display: block;
    text-align: left;
    margin: 1em auto 0.4em;
    word-break: break-word;
    width: 80%;
  }
  &__body {
    margin-top: 1em;
    margin-bottom: 1em;
  }
}
</style>
