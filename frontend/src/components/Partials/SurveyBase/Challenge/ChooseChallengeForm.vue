<template>
    <div class="chosen-challenge-form">
        <EMailListForm
                v-bind="$attrs"
                v-on="$listeners"
                v-if="challenge.name === 'EMailWhitelist'"
                :challenge="challenge"
                name="E-Mail Whitelist Challenge"
        />
        <EMailListForm
                v-bind="$attrs"
                v-on="$listeners"
                v-if="challenge.name === 'EMailBlacklist'"
                :challenge="challenge"
                name="E-Mail Blacklist Challenge"
        />
        <PasswordForm
                v-bind="$attrs"
                v-on="$listeners"
                v-if="challenge.name === 'Password'"
                :challenge="challenge"
        />
    </div>
</template>

<script>
import EMailListForm from "./EMailListForm";
import Challenge from "../../../../model/SurveyBase/Challenge/Challenge";
import PasswordForm from "./PasswordForm";

export default {
  name: "ChooseChallengeForm",
  components: {
    EMailListForm,
    PasswordForm
  },
  props: {
    challenge: {
      type: Challenge,
      required: true
    }
  }
};
</script>

<style lang="scss">
</style>
