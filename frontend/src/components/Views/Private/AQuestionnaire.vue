<template>
    <div class="a-questionnaire">
        <Questionnaire v-if="questionnaire"
                       :key="questionnaire.href"
                       :questionnaire="questionnaire"
                       :deletable="false"
                       :style="itemStyle"
                       :initiallyExpanded="true"
                       :showLink="false"
        />
    </div>
</template>

<script>
    import {mapGetters, mapState} from "vuex-fluture";
    import {isNil} from "ramda";

    import Questionnaire from "../../Partials/SurveyBase/Questionnaire";

    export default {
        name: "AQuestionnaire",
        components: {
            Questionnaire
        },
        data() {
            return {
                questionnaire: null
            };
        },
        created() {
            this.questionnaire = this
                .questionnaireById(this.$route.params.id);

            if (isNil(this.questionnaire)) {
                this.$load(
                    this.$store.dispatch(
                        "questionnaires/fetchQuestionnaire",
                        {
                            id: this.$route.params.id
                        }
                    )
                ).fork(
                    this.$handleApiError,
                    questionnaire => {
                        this.questionnaire = questionnaire;
                    }
                );
            }
        },
        computed: {
            ...mapGetters("questionnaires", ["questionnaireById"]),
            ...mapState("global", ["window"]),
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
