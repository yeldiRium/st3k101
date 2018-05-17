<template>
    <div class="surveyForSubmission-root">
        <div v-if="loading == 'loading'">
            Loading...
        </div>
        <div v-if="loading == 'done'">
            {{ $route.params.id }}
            {{ this.questionnaire }}
        </div>
        <div v-if="loading == 'error'">
            ERROR!
        </div>
    </div>
</template>

<script>
    import Questionnaire from "../../../api/Model/Questionnaire";

    export default {
        data() {
            return {
                loading: "loading",
                questionnaire: null
            };
        },
        mounted() {
            Questionnaire.get(this.$route.params.id)
                .fork(
                    data => {
                        this.loading = "error";
                    },
                    data => {
                        this.questionnaire = data;
                        this.loading = "done";
                    }
                )
        }
    }
</script>

<style lang="scss">

</style>