<template>
    <div class="a-question">
        <Question :key="question.href"
                  :question="question"
                  :deletable="false"
                  :style="itemStyle"
                  :initiallyExpanded="true"
        />
    </div>
</template>

<script>
    import {mapGetters, mapState} from "vuex-fluture";

    import Question from "../../Partials/SurveyBase/Question";

    export default {
        name: "AQuestion",
        components: {
            Question
        },
        computed: {
            ...mapGetters("questions", ["questionById"]),
            ...mapState("global", ["window"]),
            question() {
                return this.questionById(this.$route.params.id);
            },
            itemStyle() {
                let width = "1200px";
                if (this.window.width * .8 < 1200) {
                    width = "80%";
                }

                return {
                    width: width
                };
            }
        }
    }
</script>

<style lang="scss">
    .a-question {
        display: grid;
        grid-template-columns: 100%;
        grid-auto-flow: row;
        grid-row-gap: 0.5em;

        justify-items: center;
    }
</style>
