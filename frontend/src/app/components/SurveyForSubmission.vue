<template>
    <div class="surveyForSubmission-root">
        <div v-if="loading == 'loading'">
            Loading...
        </div>
        <div v-if="loading == 'done'">
            {{ $route.params.id }}
        </div>
        <div v-if="loading == 'error'">
            ERROR!
        </div>
    </div>
</template>

<script>
    import Questionnaire from "../../API/Model/Questionnaire";

    export default {
        data() {
            return {
                loading: "loading",
                questionnaire: null
            };
        },
        mounted() {
            // Doesn't work. API does not yet respect the server domain
            Questionnaire.get("blub")
                .fork(
                    data => {
                        console.error(data);
                        this.loading = "error";
                    },
                    data => {
                        console.log(data);
                        this.questionnaire = data;
                        this.loading = "done";
                    }
                )
        }
    }
</script>

<style lang="scss">

</style>