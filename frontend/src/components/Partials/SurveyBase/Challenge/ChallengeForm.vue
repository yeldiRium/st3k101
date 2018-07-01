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
                this.$emit('input', this.challenge.set(isEnabled));
            }
        }
    }
</script>

<style lang="scss">
    .challenge-form {
        &__body {
            display: grid;
            grid-template-columns: minmax(max-content, 1fr) 5fr;
            grid-row-gap: 0.2em;
        }
    }
</style>
