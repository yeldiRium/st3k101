<template>
    <div>
        <div class="survey"
             v-if="submissionQuestionnaire !== null"
        >
            <p>{{submissionQuestionnaire.name}}</p>
        </div>
        <div class="error"
             v-if="error !== null"
        >
            <p>{{error.message}}</p>
        </div>
    </div>
</template>

<script>
    import * as Future from "fluture";

    export default {
        name: "EmbeddedSurveyForSubmission",
        data() {
            return {
                submissionQuestionnaire: null,
                selectedDimensionId: null,
                error: null
            }
        },
        methods: {
            loadQuestionnaire(language = null) {
                if (typeof ltiLaunchParameters === 'undefined') {
                    return Future.reject("No LTI parameters present!");
                }
                return this.$load(
                    this.$store.dispatch(
                        "submission/fetchSubmissionQuestionnaireById",
                        {
                            id: ltiLaunchParameters.questionnaireId,
                            language: language
                        }
                    )
                );
            }
        },
        created: function () {
            this.loadQuestionnaire()
                .fork(
                    error => {
                        this.error = error;
                    },
                    questionnaire => {
                        this.submissionQuestionnaire = questionnaire;
                        if (questionnaire.dimensions.length > 0) {
                            this.selectedDimensionId = questionnaire.dimensions[0].id;
                        }
                    }
                );
        }
    }
</script>

<style lang="scss">

</style>