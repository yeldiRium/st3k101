<template>
    <div class="a-question">
        <Question v-if="question"
                  :key="question.href"
                  :question="question"
                  :deletable="false"
                  :style="itemStyle"
                  :initiallyExpanded="true"
                  @updated="reloadQuestion"
        />
    </div>
</template>

<script>
import { isNil } from "ramda";
import { mapGetters, mapState } from "vuex-fluture";

import Question from "../../Partials/SurveyBase/Question";

export default {
  name: "AQuestion",
  components: {
    Question
  },
  data() {
    return {
      question: null
    };
  },
  created() {
    this.reloadQuestion();

    if (isNil(this.question)) {
      this.$load(
        this.$store.dispatch("questions/fetchQuestion", {
          id: this.$route.params.id
        })
      ).fork(this.$handleApiError, () => {
        this.reloadQuestion();
      });
    }
  },
  computed: {
    ...mapGetters("questions", ["questionById"]),
    ...mapState("global", ["window"]),
    itemStyle() {
      let width = "1200px";
      if (this.window.width * 0.8 < 1200) {
        width = "80%";
      }

      return {
        width: width
      };
    }
  },
  methods: {
    reloadQuestion() {
      this.question = this.questionById(Number(this.$route.params.id));
    }
  }
};
</script>

<style lang="scss">
.a-question {
  display: grid;
  grid-template-columns: 100%;
  grid-auto-flow: row;
  grid-row-gap: 0.5em;

  justify-items: center;
}
</style>
