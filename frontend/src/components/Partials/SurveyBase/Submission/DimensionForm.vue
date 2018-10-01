<template>
    <div>
        <QuestionForm
                v-for="question in getQuestionsOrdered(dimension)"
                :question="question"
                :key="question.href"
                @response-change="notifyParent($event)"
        />
    </div>
</template>

<script>
import QuestionForm from "./QuestionForm";
export default {
  name: "DimensionForm",
  components: { QuestionForm },
  props: {
    dimension: null
  },
  methods: {
    notifyParent({ questionId, value }) {
      this.$emit("response-change", {
        questionId: questionId,
        value: value
      });
    },
    getQuestionsOrdered(dimension) {
      let qs = dimension.questions;
      if (!dimension.randomizeQuestionOrder) {
        return qs;
      }

      // from https://stackoverflow.com/a/12646864
      for (let i = qs.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [qs[i], qs[j]] = [qs[j], qs[i]];
      }
      return qs;
    }
  }
};
</script>

<style scoped>
</style>
