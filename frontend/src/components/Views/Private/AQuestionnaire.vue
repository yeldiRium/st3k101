<template>
    <div class="a-questionnaire">
        <Questionnaire :key="questionnaire.href"
                  :questionnaire="questionnaire"
                  :deletable="false"
                  :style="itemStyle"
                  :initiallyExpanded="true"
        />
    </div>
</template>

<script>
    import {mapGetters, mapState} from "vuex-fluture";

    import Questionnaire from "../../Partials/SurveyBase/Questionnaire";

    export default {
        name: "AQuestionnaire",
        components: {
            Questionnaire
        },
        computed: {
            ...mapGetters("questionnaires", ["questionnaireById"]),
            ...mapState("global", ["window"]),
            questionnaire() {
                return this.questionnaireById(this.$route.params.id);
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
    .a-questionnaire {
        display: grid;
        grid-template-columns: 100%;
        grid-auto-flow: row;
        grid-row-gap: 0.5em;

        justify-items: center;
    }
</style>
