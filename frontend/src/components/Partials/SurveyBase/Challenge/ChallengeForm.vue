<template>
    <div class="challenge-form">
        <div class="challenge-form__head">
            <slot name="head"></slot>
        </div>
        <div class="challenge-form__body">
            <span class="challenge-form__label">
                Enabled:
            </span>
            <ToggleButton
                    :value="this.challenge.isEnabled"
                    @input="update"
            />
            <slot name="form"></slot>
        </div>
    </div>
</template>

<script>
import Challenge from "../../../../model/SurveyBase/Challenge/Challenge";

import ToggleButton from "../../Form/ToggleButton";

export default {
  name: "ChallengeForm",
  components: {
    ToggleButton
  },
  props: {
    challenge: {
      type: Challenge,
      required: true
    }
  },
  methods: {
    update(isEnabled) {
      this.$emit("input", this.challenge.set(isEnabled));
    }
  }
};
</script>

<style lang="scss">
@import "../../../scss/_variables";

.challenge-form {
  border-left: 2px solid $primary;
  padding-bottom: 8px;
  margin-bottom: 1em;

  &__head {
    margin-bottom: 0.4em;
  }

  &__body {
    display: grid;
    grid-template-columns: minmax(max-content, 1fr) 5fr;
    grid-row-gap: 0.2em;
  }

  &__field {
    width: 100%;
    display: flex;

    > input {
      flex-grow: 3;
    }

    > button {
      flex-grow: 1;
    }
  }
}
</style>
