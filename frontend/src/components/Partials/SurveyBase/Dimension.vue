<template>
    <div class="dimension"
         :class="classes"
    >
        <ListItem class="dimension__title"
                  :value="dimension.name"
                  :subtext="subtext"
                  :mini="expanded"
                  :ellipseText="!expanded"
                  :disabled="!isEditable(dimension)"
                  @input="updateDimension('name', $event, true)"
        >
            <template>
                <IconExpandLess class="list-item__icon"
                                v-if="expanded"
                                @click.native="toggleExpanded"
                />
                <IconExpandMore class="list-item__icon"
                                v-else
                                @click.native="toggleExpanded"
                />
            </template>
            <LanguagePicker class="list-item__language-picker"
                            :language-data="dimension.languageData"
                            @choose-language="changeLanguage"
                            @choose-language-unavailable="openAddNewTranslationDialog"
            />
        </ListItem>

        <div class="dimension__body"
             v-if="expanded"
             ref="dropdown"
        >
            <!-- List of Questions -->
            <div class="dimension__questions">
                <Question class="question--bordered"
                          v-for="question in questionsOrdered"
                          :key="question.href"
                          :question="question"
                          :deletable="dimension.isConcrete"
                          @question-delete="deleteQuestion"
                />

            </div>

            <!-- Add, Delete Buttons -->
            <div class="dimension__buttons"
                 v-if="expanded"
            >
                <Button v-if="isEditable(dimension)"
                        @action="openNewQuestionDialog"
                >
                    Add new Question
                </Button>
                <Button v-if="isEditable(dimension)"
                        @action="openUseQuestionTemplateDialog"
                >
                    Use Question template
                </Button>
                <Button v-if="isDeletable(dimension)"
                        @action="deleteDimension"
                        :class="{'button--grey': dimension.isShadow}"
                >
                    Delete
                </Button>
                <Button v-if="isMakeTemplateButtonShown && !dimension.template"
                        @action="toggleIsTemplate"
                >
                    Publish as template
                </Button>
                <Button v-if="isMakeTemplateButtonShown && dimension.template"
                        @action="toggleIsTemplate"
                >
                    Retract template
                </Button>
                <Button v-if="isEditable(dimension)"
                        @action="openUpdateAllRangeLabelsDialog"
                >
                    Update all range labels
                </Button>
            </div>

            <!-- Preferences -->
            <Collapsible>
                <span slot="head">Preferences</span>
                <div slot="body" class="dimension__preferences">
                    <template>
                        <template v-if="dimension.isConcrete">
                            <span class="dimension__table-label">
                                References:
                            </span>
                            <ReferenceCounter :object="dimension"/>
                        </template>
                        <template v-else>
                            <span class="dimension__table-label dimension__table-label--span-2">
                                <router-link :to="{name: 'ADimension', params: {id: dimension.referenceTo.id}}">Go to template</router-link>
                            </span>
                        </template>
                    </template>

                    <span class="dimension__table-label">
                        xAPI ID:
                    </span>
                    <template>
                        <EditableText v-if="dimension.isConcrete"
                                      :value="dimension.referenceId"
                                      @input="updateDimension('referenceId', $event, true)"
                                      :edit-left="true"
                        />
                        <div v-else>
                            {{ dimension.referenceId }}
                        </div>
                    </template>

                    <span class="questionnaire__table-label">
                        Randomize Question order:
                    </span>
                    <Toggle :value="dimension.randomizeQuestions"
                            :disabled="!isOwnedByCurrentDataClient(dimension)"
                            @input="updateDimension('randomizeQuestions', $event)"
                    >
                    </Toggle>
                </div>
            </Collapsible>

            <!-- Tracker Entries -->
            <TrackerEntries :surveyBase="dimension"></TrackerEntries>
        </div>
    </div>
</template>

<script>
import { mapState } from "vuex-fluture";
import { assoc } from "ramda";

import { Dimension } from "../../../model/SurveyBase/Dimension";

import SurveyBase from "./SurveyBase";
import Question from "./Question";
import ListItem from "../List/Item";
import LanguagePicker from "../LanguagePicker";
import ReferenceCounter from "./Config/ReferenceCounter";
import Toggle from "../Form/ToggleButton";
import Button from "../Form/Button";
import EditableText from "../Form/EditableText";
import TrackerEntries from "./TrackerEntries";

import IconExpandLess from "../../../assets/icons/baseline-expand_less-24px.svg";
import IconExpandMore from "../../../assets/icons/baseline-expand_more-24px.svg";
import Collapsible from "../Collapsible";
import Roles, { isAtLeast } from "../../../model/Roles";
import * as R from "ramda";
import * as Future from "fluture/index.js";

export default {
  name: "Dimension",
  extends: SurveyBase,
  components: {
    Collapsible,
    ListItem,
    Question,
    LanguagePicker,
    ReferenceCounter,
    Toggle,
    Button,
    EditableText,
    TrackerEntries,
    IconExpandLess,
    IconExpandMore
  },
  props: {
    /** @type {Dimension} */
    dimension: {
      type: Dimension
    },
    initiallyExpanded: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      expanded: false,
      header: {
        height: 0
      },
      dropdown: {
        height: 0
      }
    };
  },
  computed: {
    ...mapState("session", ["dataClient"]),
    isMakeTemplateButtonShown() {
      return (
        isAtLeast(this.dataClient, Roles.Contributor) &&
        this.isEditable(this.dimension)
      );
    },
    classes() {
      return {
        "dimension--disabled": !this.isEditable(this.dimension)
      };
    },
    /**
     * Returns a message displaying the number of Questions in the Di-
     * mension.
     *
     * @returns {string}
     */
    subtext() {
      return `Contains ${this.dimension.questions.length} questions.`;
    },
    questionsOrdered() {
      return R.sortBy(R.prop("id"), this.dimension.questions);
    }
  },
  methods: {
    toggleExpanded() {
      this.expanded = !this.expanded;
    },
    /**
     * Switch the Dimension to the given language.
     * @param {Language} language
     */
    changeLanguage(language) {
      this.$load(
        this.$store.dispatch("dimensions/fetchDimension", {
          href: this.dimension.href,
          language
        })
      ).fork(this.$handleApiError, () => {
        this.$emit("updated");
      });
    },
    /**
     * Opens a dialog for entering a new translation.
     *
     * @param {Language} language
     */
    openAddNewTranslationDialog(language) {
      if (!this.isEditable(this.dimension)) {
        return;
      }
      this.$modal.show("modal-translate-dimension", {
        language,
        handler: this.addNewTranslation,
        name: this.dimension.name
      });
    },
    /**
     * Add a new translation to the Dimension.
     * This means set new field values via API for the given languages
     * and then fetch the Dimension anew in the now existing language.
     * @param {Language} language
     * @param {String} name
     */
    addNewTranslation({ language, name }) {
      if (!this.isEditable(this.dimension)) {
        return;
      }

      this.$load(
        this.$store
          .dispatch("dimensions/updateDimension", {
            dimension: this.dimension,
            language,
            params: {
              name
            }
          })
          .chain(dimension =>
            this.$store.dispatch("dimensions/fetchDimension", {
              href: dimension.href
            })
          )
      ).fork(this.$handleApiError, () => {
        this.$emit("updated");
      });
    },
    /**
     * Generically updates the Dimension via the Store.
     *
     * @param {String} prop The name of the updated property.
     * @param {*} value The new value for it.
     * @param {Boolean} mustBeEditable Whether the Dimension must be
     *  editable for this to work.
     */
    updateDimension(prop, value, mustBeEditable = false) {
      if (mustBeEditable && !this.isEditable(this.dimension)) {
        return;
      }
      this.$load(
        this.$store.dispatch("dimensions/updateDimension", {
          dimension: this.dimension,
          params: assoc(prop, value, {})
        })
      ).fork(this.$handleApiError, () => {
        this.$emit("updated");
      });
    },
    openUseQuestionTemplateDialog() {
      this.$load(
        this.$store.dispatch("questions/fetchQuestionTemplates", {})
      ).fork(this.$handleApiError, () => {
        this.$modal.show("modal-use-question-template", {
          handler: this.useQuestionTemplate
        });
      });
    },
    useQuestionTemplate({ question }) {
      this.$load(
        this.$store.dispatch("dimensions/addShadowQuestion", {
          dimension: this.dimension,
          concreteQuestion: question
        })
      ).fork(this.$handleApiError, () => {
        this.$emit("updated");
      });
    },
    openNewQuestionDialog() {
      if (!this.isEditable(this.dimension)) {
        return;
      }
      this.$modal.show("modal-create-question", {
        language: this.dimension.languageData.currentLanguage,
        handler: this.createQuestion
      });
    },
    createQuestion({ text, range }) {
      if (!this.isEditable(this.dimension)) {
        return;
      }
      this.$load(
        this.$store.dispatch("dimensions/addConcreteQuestion", {
          dimension: this.dimension,
          params: {
            text,
            range
          }
        })
      ).fork(this.$handleApiError, () => {
        this.$emit("updated");
      });
    },
    /**
     * Only handles removal from the dimension in reaction to Question
     * being deleted.
     */
    deleteQuestion(question) {
      if (!this.isEditable(this.dimension)) {
        return;
      }
      this.$load(
        this.$store.dispatch("dimensions/removeQuestion", {
          dimension: this.dimension,
          question
        })
      ).fork(this.$handleApiError, () => {
        this.$emit("updated");
      });
    },
    /**
     * Asks for confirmation, if the Dimension should be deleted, and
     * emits event that commands to do so, if the users confirms.
     */
    deleteDimension() {
      this.$modal.show("dialog", {
        title: `Really delete Dimension?`,
        text: `Do you really want to delete Dimension "${
          this.dimension.name
        }"?`,
        buttons: [
          {
            text: "Cancel"
          },
          {
            text: "Confirm",
            handler: () => this.$emit("dimension-delete", this.dimension),
            default: true
          }
        ]
      });
    },
    /**
     * Publishes / Retracts this dimension as a template.
     * TODO: prompt dataclient when there are still incoming
     * references
     * TODO: what is the correct behaviour in aforementioned
     * case?
     */
    toggleIsTemplate() {
      if (!this.isEditable(this.dimension)) {
        return; // can't publish other people's content
      }

      let template = !this.dimension.template;

      const cancel = this.$load(
        this.$store
          .dispatch("dimensions/updateDimension", {
            dimension: this.dimension,
            params: {
              template
            }
          })
          .chain(dimension =>
            this.$store.dispatch("dimensions/fetchDimension", {
              href: dimension.href,
              language
            })
          )
      ).fork(this.$handleApiError, () => {
        this.$emit("updated");
      });
    },
    openUpdateAllRangeLabelsDialog() {
      this.$modal.show("modal-updateAllRangeLabels", {
        dimension: this.dimension,
        handler: this.updateAllRangeLabels
      });
    },
    updateAllRangeLabels(rangeStartLabel, rangeEndLabel) {
      const futures = R.map(
        question =>
          this.$store.dispatch("questions/updateQuestion", {
            question,
            params: {
              range: {
                startLabel: rangeStartLabel,
                endLabel: rangeEndLabel
              }
            }
          }),
        R.filter(R.propEq("isShadow", false), this.dimension.questions)
      );
      this.$load(Future.parallel(Infinity, futures)).fork(
        this.$handleApiError,
        () => {}
      );
    }
  },
  created() {
    this.expanded = this.initiallyExpanded;
  }
};
</script>

<style lang="scss">
@import "../../scss/_variables";

.dimension {
  display: flex;
  flex-flow: column;

  background-color: $primary-light;

  &--disabled {
    background-color: $lighter;
  }

  &--bordered {
    border: 1px solid $primary;

    &.dimension--disabled {
      border-color: $slightlylight;
    }
  }

  &__add-question-button {
    background-color: $primary;
  }

  &__body {
    padding: 0.5em 2em 0.5em 2em;

    display: grid;
    grid-template-columns: minmax(max-content, 1fr) 5fr;
    grid-row-gap: 0.5em;
    align-items: center;

    > *:not(.dimension__questions) {
      text-align: center;
    }
  }

  &__preferences {
    display: grid;
    grid-template-columns: minmax(max-content, 1fr) 5fr;
    grid-row-gap: 0.5em;
    align-items: center;
    text-align: center;
  }

  &__table-label {
    padding: 0 0.5em 0 0.5em;

    &--span-2 {
      grid-column: 1 / span 2;
    }
  }

  &__questions {
    width: 100%;

    display: flex;
    flex-flow: column;

    grid-column: 1 / span 2;
    padding-top: 1em;
    padding-bottom: 1em;
  }

  &__buttons {
    grid-column: 1 / span 2;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;

    margin-bottom: 8px;

    .button {
      margin: 0 8px 0 8px;
      background-color: $primary-light;
      border: $primary 1px solid;
    }
  }

  .toggle-button {
    > div {
      color: $darker;
    }

    &--off-side.toggle-button__off-side--active,
    &--on-side.toggle-button__on-side--active {
      color: $verydark;
    }
  }
}
</style>
