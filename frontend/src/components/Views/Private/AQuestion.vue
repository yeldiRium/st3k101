<template>
    <div class="a-question">
        <Question :key="question.href"
                  :question="question"
                  :deletable="false"
        />
    </div>
</template>

<script>
    import {mapGetters} from "vuex-fluture";

    import Question from "../../Partials/SurveyBase/Question";

    export default {
        name: "AQuestion",
        components: {
            Question
        },
        computed: {
            ...mapGetters("questions", ["questionById"]),
            question() {
                return this.questionById(this.$route.params.id);
            }
        }
    }
</script>

<style lang="scss">

</style>
