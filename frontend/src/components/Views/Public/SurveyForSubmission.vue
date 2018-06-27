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
    export default {
        data() {
            return {
                loading: "loading",
                questionnaire: null
            };
        },
        mounted() {

        }
    }
</script>

<style lang="scss">

</style>
