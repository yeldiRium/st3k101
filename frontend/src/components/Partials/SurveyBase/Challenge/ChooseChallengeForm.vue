<template>
    <EMailWhitelistForm
            v-bind="$attrs"
            v-on="$listeners"
            v-if="challenge.name === 'EMailWhitelist'"
            :challenge="challenge"
    />
</template>

<script>
    import EMailWhitelistForm from "./EMailWhitelistForm";
    import Challenge from "../../../../model/SurveyBase/Challenge/Challenge";

    export default {
        name: "ChooseChallengeForm",
        components: {
            EMailWhitelistForm
        },
        props: {
            challenge: {
                type: Challenge,
                required: true
            }
        }
    }
</script>

<style lang="scss">

</style>
