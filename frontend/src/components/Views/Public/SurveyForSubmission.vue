<template>
    <div>
        <div class="submission"
             :style="itemStyle"
             v-if="submissionQuestionnaire !== null && !submitted"
        >
            <span class="submission__header">
                <span>{{ submissionQuestionnaire.name }}</span>
                <LanguagePicker
                        :language-data="submissionQuestionnaire.languageData"
                        :hideUnused="true"
                        :useLongNames="true"
                        @choose-language="changeLanguage"
                />
            </span>
            <div class="submission__body">
                <div class="submission__description"
                     v-if="submissionQuestionnaire.description.length > 0"
                >
                    {{submissionQuestionnaire.description}}
                </div>

                <div class="submission__dimension-tabs">
                    <div class="submission__dimension-item"
                         v-for="dimension in submissionQuestionnaire.dimensions"
                         @click.prevent="selectedDimensionId = dimension.id"
                         v-bind:class="{'submission__dimension-item--selected': selectedDimensionId === dimension.id}"
                    >
                        {{ dimensionLabel(dimension) }}
                    </div>
                </div>
                <div class="submission__dimension-body">
                    <DimensionForm
                            v-for="dimension in submissionQuestionnaire.dimensions"
                            v-show="selectedDimensionId === dimension.id"
                            :dimension="dimension"
                            :key="dimension.href"
                            @response-change="updateResponseValue($event)"
                    />
                </div>
                <div class="submission__pagination-buttons">
                    <Button @action="paginationPrevious">Previous page</Button>
                    <Button @action="paginationNext">Next page</Button>
                </div>
            </div>
            <div class="submission__footer">
                <div v-if="errors.length > 0"
                     class="submission__errors"
                >
                    <p v-for="errorMessage in errors">
                        <b>!</b>
                        {{errorMessage}}
                    </p>
                </div>

                <label>
                    <span>Email Address</span>
                    <input type="email"
                           v-model="inputData.email"
                    />
                </label>

                <label v-if="submissionQuestionnaire.passwordEnabled">
                    <span>Password</span>
                    <input type="password"
                           v-model="inputData.password"
                    >
                </label>

                <Button @action="submit"
                        :class="{'button--grey': !isReadyToSubmit}"
                >
                    <span v-if="isReadyToSubmit">
                        Submit
                    </span>
                    <span v-else>
                        Please complete the survey to submit.
                    </span>
                </Button>
            </div>
        </div>
        <ThankYou v-if="submitted"
                  :schedule="submissionQuestionnaire.schedule"
                  :notices="thankYouNotifications"
        >
        </ThankYou>
    </div>
</template>

<script>
import { mapState } from "vuex-fluture";
import { equals, findIndex } from "ramda";

import DimensionForm from "../../Partials/SurveyBase/Submission/DimensionForm";
import Button from "../../Partials/Form/Button";
import LanguagePicker from "../../Partials/LanguagePicker";
import { submitResponse } from "../../../api/Submission";
import * as R from "ramda";
import ThankYou from "../../Views/Embedded/ThankYou";

export default {
  name: "SurveyForSubmission",
  components: {
    Button,
    DimensionForm,
    LanguagePicker,
    ThankYou
  },
  data() {
    return {
      submissionQuestionnaire: null,
      inputData: {
        password: "",
        email: ""
      },
      selectedDimensionId: null,
      errors: [],
      submitted: false,
      thankYouNotifications: []
    };
  },
  computed: {
    ...mapState("global", ["window"]),
    itemStyle() {
      let width = "1200px";
      if (this.window.width * 0.8 < 1200) {
        width = "80%";
      }

      return {
        width: width
      };
    },
    questionnaireId() {
      return Number(this.$route.params.id);
    },
    isReadyToSubmit() {
      if (this.inputData.email.length < 6) {
        return false; // a@b.de ==> 6 chars
      }
      if (this.inputData.email.includes("@") === false) {
        return false;
      }
      if (
        this.submissionQuestionnaire.passwordEnabled &&
        this.inputData.password.length < 1
      ) {
        return false;
      }
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
     * Loads SubmissionQuestionnaire into vuex store and returns
     * Future of result.
     *
     * @param {Language} language
     * @returns {Future}
     */
    loadQuestionnaire(language = null) {
      return this.$load(
        this.$store.dispatch("submission/fetchSubmissionQuestionnaireById", {
          id: this.questionnaireId,
          language: language
        })
      );
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
    /**
     * Reloads SubmissionQuestionnaire in given language.
     * Updates component state to keep answers.
     *
     * @param {Language} language
     */
    changeLanguage(language) {
      this.loadQuestionnaire(language).fork(
        this.$handleApiError,
        questionnaire => {
          this.submissionQuestionnaire = this.reconstructState(questionnaire);
        }
      );
    },
    /**
     * Copies over answer values from current component state to
     * newQuestionnaire.
     *
     * @param {SubmissionQuestionnaire} newQuestionnaire
     * @returns {SubmissionQuestionnaire}
     */
    reconstructState(newQuestionnaire) {
      const previousState = this.submissionQuestionnaire;
      for (let prevDimension of previousState.dimensions) {
        let dimensionIndex = findIndex(
          equals(prevDimension),
          newQuestionnaire.dimensions
        );
        if (dimensionIndex < 0) {
          continue; // skip, dimension was removed
        }
        let newDimension = newQuestionnaire.dimensions[dimensionIndex];
        for (let prevQuestion of prevDimension.questions) {
          let questionIndex = findIndex(
            equals(prevQuestion),
            newDimension.questions
          );
          if (questionIndex < 0) {
            continue; // skip, question was removed
          }
          newDimension.questions[questionIndex].value = prevQuestion.value;
        }
      }
      return newQuestionnaire;
    },
    paginationNext() {
      let found = false;
      for (let dimension of this.submissionQuestionnaire.dimensions) {
        if (found) {
          this.selectedDimensionId = dimension.id;
          break;
        }
        if (dimension.id === this.selectedDimensionId) {
          found = true;
        }
      }
    },
    paginationPrevious() {
      let found = false;
      for (let dimension of R.reverse(
        this.submissionQuestionnaire.dimensions
      )) {
        if (found) {
          this.selectedDimensionId = dimension.id;
          break;
        }
        if (dimension.id === this.selectedDimensionId) {
          found = true;
        }
      }
    },
    /**
     * Submits response values to API.
     */
    submit() {
      if (!this.isReadyToSubmit) {
        return;
      }
      this.errors = [];
      this.$load(
        submitResponse(this.submissionQuestionnaire, this.inputData)
      ).fork(
        error => {
          if (
            R.either(
              R.propEq("name", "BadRequestError"),
              R.propEq("name", "ForbiddenError")
            )(error)
          ) {
            this.errors.push(
              "There was an error with the data you've provided. Please check your data and try again."
            );
          } else {
            this.$handleApiError(error);
          }
        },
        () => {
        this.submitted = true;
        this.thankYouNotifications.push(
          `A verification link has been sent to ${
            this.inputData.email
          }. Please follow the instructions in the email we've sent you to verify your submission.`
        );
      });
    },
    dimensionLabel(dimension) {
      let counter = this.getNumberOfIncompleteQuestions(dimension);
      let indicator = "";
      if (counter > 0) {
        indicator = " |  🤔 " + counter.toString();
      } else {
        indicator = " |  ✔️";
      }
      return dimension.name + indicator;
    }
  },
  created() {
    this.loadQuestionnaire().fork(
      error => {
        if (error.name === "NotFoundError") {
          this.$router.push({
            name: "PublicBase"
          });
        }
        this.$handleApiError(error);
      },
      questionnaire => {
        this.submissionQuestionnaire = questionnaire;
        if (questionnaire.dimensions.length > 0) {
          this.selectedDimensionId = questionnaire.dimensions[0].id;
        }
      }
    );
  }
};
</script>

<style lang="scss">
@import "../../scss/variables";

.submission {
  margin-left: auto;
  margin-right: auto;
  margin-top: 2em;

  &__header {
    display: flex;
    background-color: $primary;
    justify-content: space-between;
    padding: 1em;
    align-items: center;
  }

  &__description {
    margin-bottom: 2em;
  }

  &__body {
    padding: 1em;
    border: $primary 1px solid;
  }

  &__dimension-tabs {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
  }

  &__dimension-item {
    display: block;
    border: $slightlylight 1px solid;
    background-color: $lighter;
    padding-left: 1em;
    padding-right: 1em;
    flex-grow: 1;
    word-break: unset;

    &--selected {
      background-color: $primary;
      border: $primary 1px solid;
    }
  }

  &__dimension-body {
    border: $primary-light 1px solid;
    padding: 0.3em;
  }

  &__pagination-buttons {
    margin-top: 1em;
    display: flex;
    justify-content: space-between;
    > * {
      flex-basis: 30%;
    }
  }

  &__footer {
    display: flex;
    flex-direction: column;
    margin-top: 2em;
    padding: 1em;
    border: $primary 1px solid;

    label {
      display: flex;
      justify-content: space-between;
      margin-bottom: 1em;

      input {
        width: 45%;
      }
    }
  }

  &__errors {
    > p {
      color: $danger;
      margin-bottom: 1em;

      > b {
        color: inherit;
        font-size: x-large;
        margin-right: 1em;
      }
    }
  }
}
</style>
