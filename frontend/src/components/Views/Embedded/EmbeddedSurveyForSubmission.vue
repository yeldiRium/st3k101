<template>
    <div>
        <div v-if="submissionQuestionnaire !== null">
            <div class="embedded__survey"
                v-show="paginationAtSurvey"
            >
                <div class="embedded__header">
                    {{selectedDimension.name}}
                </div>
                <div class="embedded__main" id="scrollable-container">
                    <div v-for="dimension in submissionQuestionnaire.dimensions">
                        <div v-show="dimension.id === selectedDimension.id"><!-- pagination also -->
                            <QuestionForm v-for="question in getQuestionsOrdered(dimension)"
                                          :question="question"
                                          :key="question.href"
                                          @response-change="updateResponseValue($event)"
                                          class="make-small-pl0x"
                            />
                        </div>
                    </div>
                </div>
                <div class="embedded__footer"
                     v-if="paginationAtSurvey"
                >
                    <Button @action="paginationPrevious()">
                        ⬅️
                    </Button>
                    <div v-for="iPage in dimensionCount"
                         class="pagination__droplet"
                         :class="{'pagination__current': iPage - 1 === paginationIndex}"
                         @click="paginationGoto(iPage - 1)"
                    >
                        {{paginationLabelFor(iPage)}}
                    </div>
                    <Button @action="paginationNext()">
                        ➡️
                    </Button>
                </div>
            </div>
        </div>
        <div class="welcome"
             v-if="submissionQuestionnaire !== null"
        >
            <div v-show="paginationIndex === -1">
                <div class="welcome__title">
                    {{submissionQuestionnaire.name}}
                </div>
                <div class="welcome__description">
                    {{submissionQuestionnaire.description}}
                </div>
                <Button @action="paginationNext()">
                    Start
                </Button>
            </div>
        </div>
        <div class="submit"
             v-if="submissionQuestionnaire !== null"
        >
            <div v-show="paginationIndex === dimensionCount">
                <Button @action="submit()"
                        :class="{'button--grey': !isReadyToSubmit}"
                >
                    <p v-if="isReadyToSubmit">Submit</p>
                    <p v-else>Please complete the survey first.</p>
                </Button>
                <Button @action="paginationPrevious()">
                    Review answers
                </Button>
            </div>
        </div>
        <div class="error"
             v-if="error !== null"
        >
            <p>{{error.message}}</p>
        </div>
    </div>
</template>

<script>
import * as Future from "fluture/index.js";
import * as R from "ramda";

import Button from "../../Partials/Form/Button";
import QuestionForm from "../../Partials/SurveyBase/Submission/QuestionForm";
import { submitResponseLti } from "../../../api/Submission";
import { mapState } from "vuex-fluture";

export default {
  name: "EmbeddedSurveyForSubmission",
  components: {
    Button,
    QuestionForm
  },
  data() {
    return {
      submissionQuestionnaire: null,
      paginationIndex: -1,
      error: null,
      scrollableContainer: null
    };
  },
  computed: {
    ...mapState("session", ["sessionToken"]),
    dimensionCount() {
      if (R.isNil(this.submissionQuestionnaire)) {
        return 0;
      }
      return this.submissionQuestionnaire.dimensions.length;
    },
    paginationAtSurvey() {
      return (
        this.paginationIndex > -1 && this.paginationIndex < this.dimensionCount
      );
    },
    selectedDimension() {
      const dummy = {
        id: "⛄",
        name: "⛄",
        questions: []
      };
      if (R.isNil(this.submissionQuestionnaire) || !this.paginationAtSurvey) {
        return dummy;
      }
      return this.submissionQuestionnaire.dimensions[this.paginationIndex];
    },
    paginationLabelFor() {
      return index => {
        if (!R.isNil(this.submissionQuestionnaire)) {
          let dimension = this.submissionQuestionnaire.dimensions[index - 1]; // https://vuejs.org/v2/guide/list.html#v-for-with-a-Range
          let incompleteCount = this.getNumberOfIncompleteQuestions(dimension);
          if (incompleteCount === 0) {
            return "✔️";
          }
        }
        return index;
      };
    },
    isReadyToSubmit() {
      for (let dimension of this.submissionQuestionnaire.dimensions) {
        for (let question of dimension.questions) {
          if (question.value < 0) {
            return false;
          }
        }
      }
      return true;
    }
  },
  methods: {
    loadQuestionnaire(language = null) {
      if (typeof ltiLaunchParameters === "undefined") {
        return Future.reject("No LTI parameters present!");
      }
      return this.$load(
        this.$store.dispatch("submission/fetchSubmissionQuestionnaireById", {
          id: ltiLaunchParameters.questionnaireId,
          language: language
        })
      );
    },
    getNumberOfIncompleteQuestions(dimension) {
      let counter = 0;
      for (let iDimension of this.submissionQuestionnaire.dimensions) {
        if (dimension.id !== iDimension.id) {
          continue;
        }
        for (let question of dimension.questions) {
          if (question.value < 0) {
            counter++;
          }
        }
      }
      return counter;
    },
    /**
     * Scrolls the paginated content back to the top.
     */
    paginationScrollToTop() {
      let container = document.getElementById("scrollable-container");
      if (!R.isNil(container)) {
        container.scrollTop = 0;
      }
    },
    /**
     * Advances the pagination by one.
     */
    paginationNext() {
      if (this.paginationIndex === this.dimensionCount + 1) {
        return;
      }
      this.paginationIndex++;
      this.paginationScrollToTop();
    },
    /**
     * Returns to the previous page.
     */
    paginationPrevious() {
      if (this.paginationIndex === -1) {
        return;
      }
      this.paginationIndex--;
      this.paginationScrollToTop();
    },
    paginationGoto(index) {
      if (index > -1 && index < this.dimensionCount) {
        this.paginationIndex = index;
        this.paginationScrollToTop();
      }
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
    },
    /**
     * Updates response value for given questionId in component state.
     *
     * @param {String} questionId
     * @param {Integer} value
     */
    updateResponseValue({ questionId, value }) {
      for (let dimension of this.submissionQuestionnaire.dimensions) {
        for (let question of dimension.questions) {
          if (question.id === questionId) {
            question.value = value;
          }
        }
      }
    },
    submit() {
      if (!this.isReadyToSubmit) {
        return;
      }
      this.$load(
        submitResponseLti(this.submissionQuestionnaire, this.sessionToken)
      ).fork(this.$handleApiError, () => {
        this.$router.push("/embedded/thank-you");
      });
    }
  },
  created: function() {
    this.loadQuestionnaire().fork(
      error => {
        // TODO: if ForbiddenError, then survey is not published
        this.error = error;
      },
      questionnaire => {
        // TODO: redirect datasubject if survey has concluded
        /*if (questionnaire.concluded) {
                            this.$router.push("/embedded/concluded");
                        }*/
        console.log(questionnaire.dimensions);
        this.submissionQuestionnaire = questionnaire;
      }
    );
  }
};
</script>

<style lang="scss">
@import "../../scss/variables";

.welcome {
  &__title {
    font-size: large;
  }
  &__description {
    font-size: small;
  }
}

.error {
}

.embedded {
  &__survey {
    height: 100vh;
    background-color: $primary-light;
  }
  &__header {
    position: absolute;
    top: 0px;
    left: 0px;
    right: 0px;
    overflow: hidden;
    text-align: center;
    margin: 0 auto 0 auto;
    height: 1.5em;
  }
  &__footer {
    height: 2.1em;
    display: flex;
    flex-direction: row;
    justify-content: space-between;

    position: absolute;
    bottom: 0px;
    left: 0px;
    right: 0px;
    overflow: hidden;
  }
  &__main {
    background-color: white;
    position: absolute;
    top: 1.5em;
    bottom: 2.1em;
    left: 0px;
    right: 0px;
    overflow: auto;
    width: 100vw;
  }
}

.dimension-title {
  width: 100vw;
  margin: 0 auto 0 auto;
  font-size: large;
}

.make-small-pl0x {
  font-size: small !important;
}

.pagination {
  &__droplet {
    text-align: center;

    width: 100%;

    font-size: small;
    padding: 0 auto 0 auto;
  }
  &__current {
    text-align: center;
    width: 100%;
    background-color: $primary;
    padding: 0 auto 0 auto;
  }
}
</style>
