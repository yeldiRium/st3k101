<template>
    <div v-if="submissionQuestionnaire !== null">
        <div v-if="!userHasSubmitted">
            <div class="welcome">
                <WelcomePage :title="submissionQuestionnaire.name"
                             :text="submissionQuestionnaire.description"
                             v-if="paginationIndex === -1 && submissionQuestionnaire.acceptsSubmissions"
                             @startClicked="paginationNext()"
                >
                </WelcomePage>
                <LandingPage v-else-if="paginationIndex === -1 && !submissionQuestionnaire.acceptsSubmissions"
                             :questionnaire="submissionQuestionnaire"
                             @action="paginationNext()"
                >
                </LandingPage>
            </div>
            <div class="embedded__survey"
                v-show="paginationAtSurvey"
            >
                <div class="embedded__header">
                    {{selectedDimension.name}}
                </div>
                <div class="embedded__main scrollbox" id="scrollable-container">
                    <div v-for="dimension in submissionQuestionnaire.dimensions">
                        <div v-show="dimension.id === selectedDimension.id"><!-- pagination also -->
                            <QuestionForm :key="question.href"
                                          v-for="question in getQuestionsOrdered(dimension)"
                                          :question="question"
                                          @response-change="updateResponseValue($event)"
                                          class="embedded__question"
                            />
                        </div>
                    </div>
                </div>
                <div class="embedded__footer"
                     v-if="paginationAtSurvey"
                >
                    <div v-for="iPage in dimensionCount"
                         class="pagination__droplet"
                         :class="{'pagination__current': iPage - 1 === paginationIndex}"
                         @click="paginationGoto(iPage - 1)"
                    >
                        {{iPage}}
                        <div class="badge"
                             :class="{'badge__current': iPage - 1 === paginationIndex}"
                             v-bind:data-badge="answerCountLabelFor(iPage)"
                        >

                        </div>
                    </div>
                    <Button @action="paginationNext()"
                            class="next"
                    >
                        <IconNext></IconNext>
                    </Button>
                </div>
            </div>
            <div class="submit"
             v-show="paginationIndex === dimensionCount"
            >
                <div class="card">
                    <h1>
                        Ready to submit your answers?
                    </h1>
                    <p>You can review your answers before submitting by clicking the button at the bottom of this screen.</p>
                    <Button @action="submit()"
                            :class="{'button--grey': !isReadyToSubmit}"
                            class="submit__submit"
                    >
                        <p v-if="isReadyToSubmit">Submit</p>
                        <p v-else>Please complete the survey first.</p>
                    </Button>
                </div>
                <Button @action="paginationPrevious()"
                        class="submit__previous"
                >
                    <IconPrevious></IconPrevious>
                </Button>
            </div>
        </div>
        <ThankYou v-else
                  :schedule="submissionQuestionnaire.schedule"
        >
        </ThankYou>
        <div class="error"
             v-if="error !== null"
        >
            <h1 class="error__heading">Oops!</h1>
            <p class="error__text">An error occurred while launching the survey. Please contact the responsible Instructor to resolve this issue.</p>
            <p class="error__reason">Reason: {{error.message}}</p>
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
import WelcomePage from "./Partials/WelcomePage";
import ThankYou from "./ThankYou";
import LandingPage from "../../Partials/LandingPage";
import IconPrevious from "../../../assets/icons/baseline-navigate_before-24px.svg";
import IconNext from "../../../assets/icons/baseline-navigate_next-24px.svg";

export default {
  name: "EmbeddedSurveyForSubmission",
  components: {
    LandingPage,
    ThankYou,
    WelcomePage,
    Button,
    QuestionForm,
    IconPrevious,
    IconNext
  },
  data() {
    return {
      submissionQuestionnaire: null,
      paginationIndex: -1,
      error: null,
      scrollableContainer: null,
      questionOrderPerDimension: {},
      userHasSubmitted: false
    };
  },
  computed: {
    ...mapState("global", ["window"]),
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
    answerCountLabelFor() {
      return index => {
        if (!R.isNil(this.submissionQuestionnaire)) {
          let dimension = this.submissionQuestionnaire.dimensions[index - 1]; // https://vuejs.org/v2/guide/list.html#v-for-with-a-Range
          let incompleteCount = this.getNumberOfIncompleteQuestions(dimension);
          let buttonWidth = this.window.width / this.dimensionCount;

          if (incompleteCount === 0) {
            if (buttonWidth > 200) {
              return "Completed! 🎉";
            }
            return "🎉";
          }
          return `${dimension.questions.length - incompleteCount} / ${
            dimension.questions.length
          }`;
        }
        return "";
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
      if (!this.submissionQuestionnaire.acceptsSubmissions) {
        if (this.paginationIndex === this.dimensionCount - 1) {
          return;
        }
      }
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

      if (this.questionOrderPerDimension.hasOwnProperty(dimension.id)) {
        return this.questionOrderPerDimension[dimension.id];
      }

      // from https://stackoverflow.com/a/12646864
      for (let i = qs.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [qs[i], qs[j]] = [qs[j], qs[i]];
      }
      this.questionOrderPerDimension[dimension.id] = qs;
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
        this.userHasSubmitted = true;
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
  margin: 4em;

  &__reason {
    margin-top: 2em;
    font-size: small;
  }
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
    word-wrap: break-spaces;
    text-align: center;
    margin: 0 auto 0 auto;
    //height: 2em;

    font-size: large;
  }
  &__footer {
    height: 2em;
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
    top: 2em;
    bottom: 2em;
    left: 0px;
    right: 0px;
    overflow: auto;
    width: 100vw;
  }

  &__question {
    max-width: 90%;
    margin: auto;
  }
}

.pagination {
  &__droplet {
    text-align: left;
    font-size: large;
    width: 66%;
    padding-left: 1em;
    border-right: $primary-dark 1px solid;
    transition: width 0.33s ease, background-color 0.33s ease,
      font-size 0.33s ease, font-weight 0.33s ease;
  }
  &__droplet:hover {
    background-color: $secondary-light;
  }
  &__current {
    width: 100%;
    color: white;
    vertical-align: center;
    background-color: $primary;
    padding: 0 auto 0 auto;
    font-weight: bolder;
  }
  &__current:hover {
    background-color: $primary;
  }
}

.badge {
  position: relative;

  &__current {
    color: white;
  }
}

.badge[data-badge]:after {
  content: attr(data-badge);
  position: absolute;
  right: 1em;
  top: -1.5em;
  font-size: small;
  text-align: center;
}

.scrollbox {
  overflow: auto;

  background:
		/* Shadow covers */ linear-gradient(
      white 30%,
      rgba(255, 255, 255, 0)
    ),
    linear-gradient(rgba(255, 255, 255, 0), white 70%) 0 100%,
    /* Shadows */
      radial-gradient(
        50% 0,
        farthest-side,
        rgba(0, 0, 0, 0.2),
        rgba(0, 0, 0, 0)
      ),
    radial-gradient(
        50% 100%,
        farthest-side,
        rgba(0, 0, 0, 0.2),
        rgba(0, 0, 0, 0)
      )
      0 100%;
  background:
		/* Shadow covers */ linear-gradient(
      white 30%,
      rgba(255, 255, 255, 0)
    ),
    linear-gradient(rgba(255, 255, 255, 0), white 70%) 0 100%,
    /* Shadows */
      radial-gradient(
        farthest-side at 50% 0,
        rgba(0, 0, 0, 0.2),
        rgba(0, 0, 0, 0)
      ),
    radial-gradient(
        farthest-side at 50% 100%,
        rgba(0, 0, 0, 0.2),
        rgba(0, 0, 0, 0)
      )
      0 100%;
  background-repeat: no-repeat;
  background-color: white;
  background-size: 100% 40px, 100% 40px, 100% 14px, 100% 14px;

  /* Opera doesn't support this in the shorthand */
  background-attachment: local, local, scroll, scroll;
}

.submit {
  &__submit {
    margin-top: 12%;
    font-size: x-large;
    width: auto;
  }

  &__previous {
    position: absolute;
    bottom: 0;
    width: 16.6vw;
  }
}

.next {
  width: 16.6vw;
}

.card {
  margin: 10%;
}
</style>
