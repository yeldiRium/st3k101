<template>
    <div class="a-questionnaire">
        <Questionnaire v-if="questionnaire"
                       :key="questionnaire.href"
                       :questionnaire="questionnaire"
                       :deletable="false"
                       :style="itemStyle"
                       :initiallyExpanded="true"
                       :showLink="false"
                       @updated="reloadQuestionnaire"
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
            this.reloadQuestionnaire();

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
                    ()=> {
                        this.reloadQuestionnaire()
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
        },
        methods: {
            reloadQuestionnaire() {
                this.questionnaire = this.questionnaireById(
                    Number(this.$route.params.id)
                );
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
