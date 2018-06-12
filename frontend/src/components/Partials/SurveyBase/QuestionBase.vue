<template>
</template>

<script>
    import {Question} from "../../../model/SurveyBase/Question";

    import SurveyBase from "./SurveyBase";

    /**
     * Defines some properties and computed propertes for Questions.
     */
    export default {
        name: "QuestionBase",
        extends: SurveyBase,
        props: {
            /** @type {Question} */
            question: {
                type: Question
            }
        }
    }
</script>

<style lang="scss">
</style>
