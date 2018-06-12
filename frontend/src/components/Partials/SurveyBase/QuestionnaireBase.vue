<template>
</template>

<script>
    import Questionnaire from "../../../model/SurveyBase/Questionnaire";

    import SurveyBase from "./SurveyBase";

    /**
     * Defines some properties and computed propertes for Dimensions.
     */
    export default {
        name: "QuestionnaireBase",
        extends: SurveyBase,
        props: {
            /** @type {Questionnaire} */
            questionnaire: {
                type: Questionnaire
            }
        }
    }
</script>

<style lang="scss">
</style>
