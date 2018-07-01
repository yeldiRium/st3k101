<template>
    <ChallengeForm
            v-bind="$attrs"
            v-on="$listeners"
            :challenge="challenge"
    >
        <span slot="head">
            E-Mail Whitelist Challenge
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
    import EMailWhitelist from "../../../../model/SurveyBase/Challenge/EMailWhitelist";

    export default {
        name: "EMailWhitelistForm",
        components: {
            ChallengeForm
        },
        props: {
            challenge: {
                type: EMailWhitelist,
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

                this.$emit(
                    'input',
                    new EMailWhitelist(
                        this.challenge.isEnabled,
                        elems
                    )
                );
            }
        }
    }
</script>

<style lang="scss">

</style>
