<template>
    <ChallengeForm
            v-bind="$attrs"
            v-on="$listeners"
            :challenge="challenge"
    >
        <span slot="head">
            {{ name }}
        </span>
        <template slot="form">
            <span class="challenge-form__label">
                E-Mail List:
            </span>
            <div class="challenge-form__field">
                <input v-model="templist" @keyup.enter="setList"/>
                <button @click="setList">Set</button>
            </div>
        </template>
    </ChallengeForm>
</template>

<script>
    import {all, join, map, pipe, split, test, trim} from "ramda";

    import ChallengeForm from "./ChallengeForm";
    import EMailListBase from "../../../../model/SurveyBase/Challenge/EMailListBase";

    export default {
        name: "EMailListForm",
        components: {
            ChallengeForm
        },
        props: {
            challenge: {
                type: EMailListBase,
                required: true
            },
            name: {
                type: String,
                required: true
            }
        },
        data() {
            return {
                templist: ""
            };
        },
        watch: {
            challenge: {
                immediate: true,
                handler(newChallenge) {
                    this.templist = join(", ", this.challenge.emails);
                }
            }
        },
        methods: {
            setList() {
                const elems = pipe(
                    split(","),
                    map(trim)
                )(this.templist);

                if (!all(test(/.*@.*\..*/), elems)) {
                    alert("The E-Mail list must be a comma-separated list of valid E-Mails.");
                    return;
                }

                const newChallenge = this.challenge.clone();
                newChallenge.emails = elems;

                this.$emit(
                    'input',
                    newChallenge
                );
            }
        }
    }
</script>

<style lang="scss">

</style>
