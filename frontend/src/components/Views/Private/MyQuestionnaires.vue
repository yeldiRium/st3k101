<template>
    <div class="my-questionnaires">
        <div class="my-questionnaires__questionnaires">
            <Questionnaire :style="itemStyle"
                           v-for="questionnaire in myQuestionnairesOrdered"
                           :key="questionnaire.href"
                           :questionnaire="questionnaire"
                           @questionnaire-delete="deleteQuestionnaire(questionnaire)"
            />
        </div>

        <TrackerEntries :all="true" :style="itemStyle" class="collapsible--primary-light"></TrackerEntries>

        <div class="my-questionnaires__buttons">
            <Button class="my-questionnaires__add-questionnaire-button"
                    @action="openNewQuestionnaireDialog"
            >
                Add new Questionnaire
            </Button>
            <Button class="my-questionnaires__use-template-button"
                    @action="openUseQuestionnaireTemplateDialog"
            >
                Use Questionnaire template
            </Button>
        </div>
    </div>
</template>

<script>
import { mapGetters, mapState } from "vuex-fluture";
import * as R from "ramda";

import Button from "../../Partials/Form/Button";
import Questionnaire from "../../Partials/SurveyBase/Questionnaire";
import TrackerEntries from "../../Partials/SurveyBase/TrackerEntries";

export default {
  name: "MyQuestionnaires",
  components: {
    TrackerEntries,
    Button,
    Questionnaire
  },
  computed: {
    ...mapState("session", ["dataClient"]),
    ...mapGetters("questionnaires", ["myQuestionnaires"]),
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
    myQuestionnairesOrdered() {
      return R.sortBy(R.prop("id"), this.myQuestionnaires);
    }
  },
  methods: {
    /**
     * Open the loading... modal;
     * Load the Questionnaires owned by the current DataClient from the
     * API;
     * Close the loading... modal
     */
    openUseQuestionnaireTemplateDialog() {
      this.$load(
        this.$store.dispatch("questionnaires/fetchQuestionnaireTemplates", {})
      ).fork(this.$handleApiError, () => {
        this.$modal.show("modal-use-questionnaire-template", {
          handler: this.useQuestionnaireTemplate
        });
      });
    },
    useQuestionnaireTemplate({ questionnaire }) {
      this.$load(
        this.$store.dispatch("questionnaires/createShadowQuestionnaire", {
          concreteQuestionnaire: questionnaire
        })
      ).fork(this.$handleApiError, () => {});
    },
    openNewQuestionnaireDialog() {
      this.$modal.show("modal-create-questionnaire", {
        language: this.dataClient.language,
        handler: this.createQuestionnaire
      });
    },
    createQuestionnaire({
      name,
      description,
      isPublic,
      allowEmbedded,
      xapiTarget,
      language
    }) {
      this.$load(
        this.$store.dispatch("questionnaires/createConcreteQuestionnaire", {
          language: language,
          name,
          description,
          isPublic,
          allowEmbedded,
          xapiTarget
        })
      ).fork(this.$handleApiError, () => {});
    },
    deleteQuestionnaire(questionnaire) {
      this.$load(
        this.$store.dispatch("questionnaires/deleteQuestionnaire", {
          questionnaire
        })
      ).fork(this.$handleApiError, () => {});
    }
  }
};
</script>

<style lang="scss">
@import "../../scss/_variables";

.my-questionnaires {
  display: grid;
  grid-template-columns: 100%;
  grid-auto-flow: row;
  grid-row-gap: 0.5em;

  justify-items: center;

  &__questionnaires {
    width: 100%;

    display: grid;
    grid-template-columns: 100%;
    grid-auto-flow: row;
    grid-row-gap: 0.5em;

    justify-items: center;
  }

  &__buttons {
    display: grid;
    grid-auto-flow: column;
    grid-column-gap: 0.5em;
  }
}
</style>
