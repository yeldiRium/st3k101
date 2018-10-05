<template>
    <div id="app">
        <router-view/>
        <notifications
                position="top right"
        />
        <Dialog ref="modal-dialog"/>
        <LoadingSpinnerModal
                :size="width"
                ref="modal-loadingSpinner"
        />
        <CreateQuestion ref="modal-createQuestion"/>
        <CreateDimension ref="modal-createDimension"/>
        <CreateQuestionnaire ref="modal-createQuestionnaire"/>
        <UseQuestionTemplate ref="modal-useQuestionTemplate"/>
        <UseDimensionTemplate ref="modal-useDimensionTemplate"/>
        <UseQuestionnaireTemplate ref="modal-useQuestionnaireTemplate"/>
        <TranslateQuestion ref="modal-translateQuestion"/>
        <TranslateDimension ref="modal-translateDimension"/>
        <TranslateQuestionnaire ref="modal-translateQuestionnaire"/>
        <ForgetDataSubject ref="modal-forgetDataSubject"/>
        <UpdateAllRangeLabels ref="modal-updateAllRangeLabels"/>
    </div>
</template>

<script>
import * as R from "ramda";
import { mapState, mapGetters } from "vuex-fluture";

import Dialog from "./Partials/Modal/Dialog";
import CreateQuestion from "./Partials/Modal/CreateQuestion";
import CreateDimension from "./Partials/Modal/CreateDimension";
import CreateQuestionnaire from "./Partials/Modal/CreateQuestionnaire";
import UseQuestionTemplate from "./Partials/Modal/UseQuestionTemplate";
import UseDimensionTemplate from "./Partials/Modal/UseDimensionTemplate";
import UseQuestionnaireTemplate from "./Partials/Modal/UseQuestionnaireTemplate";
import TranslateQuestion from "./Partials/Modal/TranslateQuestion";
import TranslateDimension from "./Partials/Modal/TranslateDimension";
import TranslateQuestionnaire from "./Partials/Modal/TranslateQuestionnaire";
import ForgetDataSubject from "./Partials/Modal/ForgetDataSubject";
import UpdateAllRangeLabels from "./Partials/Modal/UpdateAllRangeLabels";

export default {
  components: {
    ForgetDataSubject,
    UpdateAllRangeLabels,
    Dialog,
    CreateQuestion,
    CreateDimension,
    CreateQuestionnaire,
    UseQuestionTemplate,
    UseDimensionTemplate,
    UseQuestionnaireTemplate,
    TranslateQuestion,
    TranslateDimension,
    TranslateQuestionnaire
  },
  watch: {
    isLoggedIn: {
      immediate: true,
      handler() {
        for (const ref in this.$refs) {
          if (R.length(R.match(/^modal-.*/, ref)) > 0) {
            this.$refs[ref].close();
          }
        }
      }
    }
  },
  computed: {
    ...mapState("global", ["window"]),
    ...mapGetters("session", ["isLoggedIn"]),
    width() {
      if (this.window.width * 0.5 < 200) {
        return "50%";
      }
      return "200px";
    }
  }
};
</script>

<style lang="scss">
@import "./scss/_variables";

* {
  color: $verydark;
  font-family: "Noto Sans Light", "Arial", sans-serif;
}
</style>
