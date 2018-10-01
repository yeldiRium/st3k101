<template>
    <div id="app">
        <router-view/>
        <notifications
                position="top right"
        />
        <Dialog/>
        <LoadingSpinnerModal
                :size="width"
        />
        <CreateQuestion/>
        <CreateDimension/>
        <CreateQuestionnaire/>
        <UseQuestionTemplate/>
        <UseDimensionTemplate/>
        <UseQuestionnaireTemplate/>
        <TranslateQuestion/>
        <TranslateDimension/>
        <TranslateQuestionnaire/>
    </div>
</template>

<script>
import { mapState } from "vuex-fluture";

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

export default {
  components: {
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
  computed: {
    ...mapState("global", ["window"]),
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
  font-family: "Noto Sans Light", "Arial";
}
</style>
