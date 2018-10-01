<template>
    <ChallengeForm
            v-bind="$attrs"
            v-on="$listeners"
            :challenge="challenge"
    >
        <span slot="head">
            Password Challenge
        </span>
        <template slot="form">
            <span class="challenge-form__label">
                Password:
            </span>
            <div class="challenge-form__field">
                <input v-model="tempPassword" @keyup.enter="setPassword"/>
                <button @click="setPassword">Set</button>
            </div>
        </template>
    </ChallengeForm>
</template>

<script>
import { all, join, map, pipe, split, test, trim } from "ramda";

import ChallengeForm from "./ChallengeForm";
import Password from "../../../../model/SurveyBase/Challenge/Password";

export default {
  name: "PasswordForm",
  components: {
    ChallengeForm
  },
  props: {
    challenge: {
      type: Password,
      required: true
    }
  },
  data() {
    return {
      tempPassword: ""
    };
  },
  watch: {
    challenge: {
      immediate: true,
      handler(newChallenge) {
        this.tempPassword = this.challenge.password;
      }
    }
  },
  methods: {
    setPassword() {
      this.$emit("input", this.challenge.setPassword(this.tempPassword));
    }
  }
};
</script>

<style lang="scss">
</style>
